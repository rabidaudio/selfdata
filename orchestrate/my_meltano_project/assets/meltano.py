import json
import logging
import os
import re
import shlex
import subprocess
from typing import List

import yaml
from dagster import (
    Array,
    AssetOut,
    AssetsDefinition,
    Failure,
    Noneable,
    OpExecutionContext,
    Output,
    get_dagster_logger,
    job,
    multi_asset,
    op,
)


def sanitize_name(name: str) -> str:
    return re.sub(r"[-]", "_", name)


def _meltano_env() -> dict:
    return {
        "PATH": os.environ["PATH"],
        "MELTANO_CLI_LOG_CONFIG": "orchestrate/dagster-logging.yml",
    }


def _parse_selected_properties(data: str) -> List[str]:
    props = []
    found_selected = False
    for line in data.splitlines():
        line = line.decode("utf-8")
        if not found_selected:
            if "Selected attributes:" in line:
                found_selected = True
            continue
        match = re.match(r"\s*\[(selected|automatic)\s*\]", line)
        if match:
            end = match.end()
            props.append(line[end:].strip())

    return props


# TODO: create lock files to cache these
def _parse_unique_streams(data: str) -> List[str]:
    return set([prop.split(".")[0] for prop in _parse_selected_properties(data)])


def _execute_meltano_command(args, **kwargs) -> subprocess.CompletedProcess:
    cmd = shlex.join([".meltano/run/bin", *args])
    return subprocess.run(
        args=cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.environ["MELTANO_PROJECT_ROOT"],
        env=_meltano_env(),
        **kwargs,
    )


with open(f"{os.environ['MELTANO_PROJECT_ROOT']}/meltano.yml", "r") as f:
    MELTANO_YML = yaml.safe_load(f)


def _tap_name_to_namespace(tap: str) -> str:
    for extractor in MELTANO_YML["plugins"]["extractors"]:
        if extractor["name"] == tap and "namespace" in extractor:
            return extractor["namespace"]
    # default: guess
    return re.sub("-", "_", tap)


# TODO: convert meltano into cli resource


def get_streams(tap):
    proc = _execute_meltano_command(["select", "--list", tap])
    if proc.returncode != 0:
        raise Exception(f"meltano select failed for tap {tap}:", proc.stderr)
    return _parse_unique_streams(proc.stdout)


def meltano_run(config: dict) -> int:
    logger = get_dagster_logger()
    args = [".meltano/run/bin"]
    if config.get("environment"):
        args.append(f"--environment={config['environment']}")
    args.append("run")
    for barg in ["dry-run", "full-refresh", "no-state-update", "force"]:
        if config.get(barg):
            args.append(f"--{barg}")
    args = [*args, *config["blocks"]]

    env = _meltano_env()
    if config.get("env"):
        env.update(config["env"])

    cmd = shlex.join(args)
    sub_process = None
    try:
        logger.info(f"running {cmd}")
        sub_process = subprocess.Popen(
            args=cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.environ["MELTANO_PROJECT_ROOT"],
            env=env,
            encoding="UTF-8",
        )

        logger.info(f"Command pid: {sub_process.pid}")

        # Stream back logs as they are emitted
        for line in sub_process.stdout:
            line = line.rstrip()
            try:
                data = json.loads(line)
                level = logging.getLevelName(data["level"].upper())
                logger.log(level, data["event"])
            except json.JSONDecodeError:
                logger.info(line)

        sub_process.wait()
        logger.info("Command completed")
        if sub_process.returncode:
            raise Failure(
                description="Shell command execution failed: "
                f"{sub_process.returncode}"
            )
        return sub_process.returncode
    finally:
        # Always terminate subprocess, including in cases where the
        # pipeline run is terminated
        if sub_process:
            sub_process.terminate()


# Creating an op and job for the meltano run op is useful for testing


@op(
    config_schema={
        "blocks": Array(str),
        "env": Noneable(dict),
        "environment": Noneable(str),
        "dry-run": Noneable(bool),
        "full-refresh": Noneable(bool),
        "no-state-update": Noneable(bool),
        "force": Noneable(bool),
    }
)
def meltano_run_op(context: OpExecutionContext) -> int:
    return meltano_run(context.op_config)


@job
def meltano_run_job():
    meltano_run_op()


def meltano_el_asset(tap, target, **kwargs) -> AssetsDefinition:
    print(f"determining streams for {tap}")
    streams = get_streams(tap)
    namespace = _tap_name_to_namespace(tap)
    outs = {
        stream: AssetOut(key_prefix=namespace, dagster_type=None) for stream in streams
    }

    @multi_asset(
        name=sanitize_name(f"meltano_el_{tap}_{target}"),
        outs=outs,
        group_name="meltano_el",
    )
    def _meltano_el():
        get_dagster_logger().info(f"outs: {outs.keys()}")
        meltano_run(
            {
                "blocks": [tap, target],
                **kwargs,
            }
        )
        get_dagster_logger().info(f"outs: {outs.keys()}")
        for stream in outs.keys():
            yield Output(f"{namespace}/{stream}", output_name=stream)

    return _meltano_el


def meltano_el_assets(taps, target, **kwargs) -> List[AssetsDefinition]:
    return [meltano_el_asset(tap, target, **kwargs) for tap in taps]
