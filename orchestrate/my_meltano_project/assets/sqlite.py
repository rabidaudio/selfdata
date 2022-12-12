import os
import sqlite3
from functools import cache

from dagster import asset

from my_meltano_project.services.athena import query_athena

# Evidence doesn't support Athena, and won't accept it as a core contribution.
# https://github.com/evidence-dev/evidence/pull/473
# I cannot make a community plugin until that functionality is supported:
# https://github.com/evidence-dev/evidence/issues/472
#
# In the meantime, we load our athena queries into a local sqlite database,
# and then have Evidence query that.
# To make this simpler, evidence queries are backed by models in dbt, and then
# transferred with basic selects.


@cache
def _get_connection():
    return sqlite3.connect(f"{os.environ['MELTANO_PROJECT_ROOT']}/notebook/temp.db")


def _wipe_table(table_name):
    _get_connection().cursor().execute(f"DROP TABLE IF EXISTS {table_name}")


def create_sqlite_asset(table):
    @asset(non_argument_deps={table}, name=f"sqlite_tmp_{table}")
    def _sqlite_table():
        data = query_athena(f"SELECT * FROM analytics.{table}")
        _wipe_table(table)
        data.to_sql(name=table, con=_get_connection())

    return _sqlite_table


def sqlite_assets(tables):
    return [create_sqlite_asset(table) for table in tables]
