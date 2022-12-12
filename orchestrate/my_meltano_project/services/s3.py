import os
from functools import cache

import s3fs


@cache
def get_filesystem():
    fs = s3fs.S3FileSystem(
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    return fs


def upload_files(local_path, bucket=os.environ["WAREHOUSE_BUCKET"], root_path="/"):
    get_filesystem().put(local_path, f"{bucket}{root_path}", recursive=True)
