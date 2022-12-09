from dagster import load_assets_from_package_module, repository

from my_meltano_project import assets


@repository
def my_meltano_project():
    return [load_assets_from_package_module(assets)]
