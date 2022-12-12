import os

import yaml
from dagster import load_assets_from_package_module, repository

from my_meltano_project import assets
from my_meltano_project.assets.dbt import dbt_assets
from my_meltano_project.assets.evidence import evidence_asset
from my_meltano_project.assets.meltano import meltano_el_assets, meltano_run_job
from my_meltano_project.assets.sqlite import sqlite_assets

# TODO: will be uncessary pending https://github.com/meltano/meltano/pull/6409
WORKDIR = os.environ["MELTANO_PROJECT_ROOT"]


@repository
def my_meltano_project():
    with open(f"{WORKDIR}/dag.yml", "r") as f:
        config = yaml.safe_load(f)
        return [
            # EL
            meltano_run_job,
            *meltano_el_assets(**config["meltano_el"]),
            # DBT
            *dbt_assets(
                profile=config["dbt"]["profile"],
                project_path=f"{WORKDIR}/{config['dbt']['project_path']}",
                target_path=f"{WORKDIR}/{config['dbt']['target_path']}",
            ),
            # Evidence
            *sqlite_assets(config["evidence"]["tables"]),
            evidence_asset(
                path=f"{WORKDIR}/notebook",
                tables=config["evidence"]["tables"],
                dest="/site/",
            ),
            # Anything else
            load_assets_from_package_module(assets),
        ]
