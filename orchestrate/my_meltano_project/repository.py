import json

from dagster import load_assets_from_package_module, repository, with_resources
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_manifest
from my_meltano_project import assets
from my_meltano_project.assets.meltano import meltano_el_assets, meltano_run_job


def dbt_assets():
    with open(
        "/Users/cjk/projects/selfdata/.meltano/transformers/dbt/target/manifest.json",
        "r",
    ) as f:
        data = json.load(f)
        return with_resources(
            load_assets_from_dbt_manifest(data),
            {
                "dbt": dbt_cli_resource.configured(
                    {"project_dir": "/Users/cjk/projects/selfdata/transform"},
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
