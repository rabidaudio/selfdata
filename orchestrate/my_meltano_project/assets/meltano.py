import re
from typing import List

from dagster import (
    Array,
    AssetOut,
    AssetsDefinition,
    Noneable,
    OpExecutionContext,
    Output,
    job,
    multi_asset,
    op,
)

from my_meltano_project.services.meltano import meltano_run


def sanitize_name(name: str) -> str:
    return re.sub(r"[-]", "_", name)


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


def meltano_el_asset(
    tap: str, target: str, streams: List[str], namespace: str, **kwargs
) -> AssetsDefinition:
    @multi_asset(
        name=sanitize_name(f"meltano_el_{tap}_{target}"),
        outs={
            stream: AssetOut(key_prefix=namespace, dagster_type=None)
            for stream in streams
        },
        group_name="meltano_el",
    )
    def _meltano_el():
        meltano_run(
            {
                "blocks": [tap, target],
                **kwargs,
            }
        )
        for stream in streams:
            yield Output(f"{namespace}/{stream}", output_name=stream)

    return _meltano_el


def meltano_el_assets(
    taps: List[dict], target: str, **kwargs
) -> List[AssetsDefinition]:
    return [
        meltano_el_asset(tap_name, target, **tap, **kwargs)
        for tap_name, tap in taps.items()
    ]
