from contextlib import contextmanager

from dagster import StringSource
from dagster._core.storage.runs import SqliteRunStorage
from dagster._serdes import ConfigurableClass

from my_meltano_project.services.s3 import get_filesystem
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path

# TODO: should probably use some sort of locking mechanism


class S3SqliteRunStorage(SqliteRunStorage, ConfigurableClass):
    """
    Wrapper for SqliteRunStorage which persists the database
    in S3.
    """

    def __init__(self, conn_string, inst_data=None):
        super().__init__(conn_string, inst_data)
        self.fs = get_filesystem()
        self._base_dir = None
        self._remote_dir = None

    @contextmanager
    def connect(self):
        self._download()
        with super().connect() as conn:
            try:
                yield conn
            finally:
                self._upload()

    @classmethod
    def config_type(cls):
        return {"remote_dir": StringSource, **super().config_type()}

    @staticmethod
    def from_config_value(inst_data, config_value):
        return S3SqliteRunStorage.from_local(inst_data=inst_data, **config_value)

    @classmethod
    def from_local(cls, base_dir, remote_dir, inst_data=None):
        fs = get_filesystem()
        try:
            fs.get(f"s3://{remote_dir}/dagster", base_dir, recursive=True)
        except FileNotFoundError:
            # no worries, we'll upload one in a few.
            # write a placeholder file so the directory exists.
            with fs.open(f"s3://{remote_dir}/dagster/.keep", "w") as f:
                f.write("keep")
        inst = super().from_local(base_dir, inst_data=inst_data)
        inst._base_dir = base_dir
        inst._remote_dir = remote_dir
        inst._upload()
        return inst

    def _download(self):
        self.fs.get(
            f"s3://{self._remote_dir}/dagster",
            self._base_dir,
            recursive=True,
        )

    def _upload(self):
        # TODO: for some reason this doesn't allow copying the contents, only the whole dir
        # self.fs.put(f"{self._base_dir}/*", f"s3://{self._remote_dir}/dagster", recursive=True)
        lfs = LocalFileSystem()
        root = Path(self._base_dir).absolute()
        for path in lfs.find(self._base_dir):
            self.fs.put_file(path, f"s3://{self._remote_dir}/dagster/{Path(path).relative_to(root)}")
