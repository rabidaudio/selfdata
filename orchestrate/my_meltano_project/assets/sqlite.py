import os
import sqlite3
from functools import cache

from dagster import asset

from .athena import query_athena

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


@asset(non_argument_deps={"listens_per_month"})
def sqlite_listens_per_month():
    data = query_athena("SELECT * FROM analytics.listens_per_month")
    _wipe_table("listens_per_month")
    data.to_sql(name="listens_per_month", con=_get_connection())


@asset(non_argument_deps={"lastfm_users"})
def sqlite_lastfm_users():
    data = query_athena("SELECT * FROM analytics.lastfm_users")
    _wipe_table("lastfm_users")
    data.to_sql(name="lastfm_users", con=_get_connection())


@asset(non_argument_deps={"chess_openings"})
def sqlite_chess_openings():
    data = query_athena("SELECT * FROM analytics.chess_openings")
    _wipe_table("chess_openings")
    data.to_sql(name="chess_openings", con=_get_connection())


@asset(non_argument_deps={"chess_outcomes_by_month"})
def sqlite_chess_outcomes_by_month():
    data = query_athena("SELECT * FROM analytics.chess_outcomes_by_month")
    _wipe_table("chess_outcomes_by_month")
    data.to_sql(name="chess_outcomes_by_month", con=_get_connection())
