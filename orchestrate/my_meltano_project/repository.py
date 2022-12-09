from dagster import load_assets_from_package_module, repository

from my_meltano_project import assets
from my_meltano_project.assets.meltano import meltano_el_assets, meltano_run


@repository
def my_meltano_project():
    return [
        load_assets_from_package_module(assets),
        meltano_run,
        *meltano_el_assets([
            'tap-lichess',
            'tap-lastfm',
        ])
    ]
