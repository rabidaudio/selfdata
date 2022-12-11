import json
import os

from dagster import load_assets_from_package_module, repository, with_resources
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_manifest

from my_meltano_project import assets
from my_meltano_project.assets.meltano import meltano_el_assets, meltano_run_job

DBT_PROJECT_PATH = f"{os.environ['MELTANO_PROJECT_ROOT']}/transform"
DBT_TARGET_PATH = (
    f"{os.environ['MELTANO_PROJECT_ROOT']}/.meltano/transformers/dbt/target"
)


def dbt_assets():
    # TODO: run dbt compile first!
    with open(
        f"{DBT_TARGET_PATH}/manifest.json",
        "r",
    ) as f:
        data = json.load(f)
        return with_resources(
            load_assets_from_dbt_manifest(data),
            {
                "dbt": dbt_cli_resource.configured(
                    {
                        "project_dir": DBT_PROJECT_PATH,
                        "target_path": DBT_TARGET_PATH,
                        "profiles_dir": f"{DBT_PROJECT_PATH}/profiles/athena",
                    }
                )
            },
        )


@repository
def my_meltano_project():
    return [
        load_assets_from_package_module(assets),
        meltano_run_job,
        *meltano_el_assets(
            taps=[
                "tap-lichess",
                "tap-lastfm",
            ],
            target="target-athena",
        ),
        *dbt_assets(),
    ]
