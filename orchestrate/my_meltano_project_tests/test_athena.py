import datetime

import pandas as pd

from my_meltano_project.assets.athena import query_athena


def test_query_athena():
    data = query_athena(
        """
select
timestamp '2012-10-31 01:00 UTC' as timestamp,
timestamp '2012-10-31 01:00 UTC' AT TIME ZONE 'America/Los_Angeles' as timestamptz,
date '2012-08-08' + interval '2' day as date,
time '01:00' + interval '3' hour as time
    """
    )
    assert type(data) == pd.DataFrame
    assert [k for k in data.loc[0].to_dict().keys()] == [
        "timestamp",
        "timestamptz",
        "date",
        "time",
    ]
    assert type(data.loc[0].to_dict()["date"]) == datetime.date
    # TODO: pending PandasCursor bug
    # assert type(data.loc[0].to_dict()["timestamp"]) == datetime.datetime
