import json
import logging
import os
import shlex
import subprocess

from dagster import Failure, get_dagster_logger


def _meltano_env() -> dict:
    return {
        "PATH": os.environ["PATH"],
        "MELTANO_CLI_LOG_CONFIG": "orchestrate/dagster-logging.yml",
    }


def execute_meltano_command(args, **kwargs) -> subprocess.CompletedProcess:
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
