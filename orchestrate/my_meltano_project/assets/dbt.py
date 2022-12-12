import json

from dagster import get_dagster_logger, with_resources
from dagster_dbt import dbt_cli_resource, load_assets_from_dbt_manifest

from my_meltano_project.services.meltano import execute_meltano_command

# TODO: make dbt compile an asset


def dbt_assets(profile, project_path, target_path):
    get_dagster_logger().info("Running dbt compile")
    execute_meltano_command(["invoke", f"dbt-{profile}:compile"])
    with open(
        f"{target_path}/manifest.json",
        "r",
    ) as f:
        data = json.load(f)
        return with_resources(
            load_assets_from_dbt_manifest(data),
            {
                "dbt": dbt_cli_resource.configured(
                    {
                        "project_dir": project_path,
                        "target_path": target_path,
                        "profiles_dir": f"{project_path}/profiles/{profile}",
                    }
                )
            },
        )
