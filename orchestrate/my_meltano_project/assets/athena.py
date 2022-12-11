import os

import pandas as pd
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor


def query_athena(sql, **params) -> pd.DataFrame:
    conn = connect(
        s3_staging_dir=os.environ["WAREHOUSE_STAGING_DIR"],
        region_name=os.environ["WAREHOUSE_REGION"],
        cursor_class=PandasCursor,
    )
    return pd.read_sql_query(sql, conn, params=params)


# TODO: write to athena
