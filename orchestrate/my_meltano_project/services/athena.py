import os
from functools import cache

import pandas as pd
from pyathena import connect
from pyathena.pandas.util import as_pandas


@cache
def _get_connection():
    return connect(
        s3_staging_dir=os.environ["WAREHOUSE_STAGING_DIR"],
        region_name=os.environ["WAREHOUSE_REGION"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        # cursor_class=PandasCursor, # TODO: this doesn't work for some reason
    )


def query_athena(sql, **params) -> pd.DataFrame:
    cursor = _get_connection().cursor()
    cursor.execute(sql, params)
    return as_pandas(cursor)


# TODO: write to athena
