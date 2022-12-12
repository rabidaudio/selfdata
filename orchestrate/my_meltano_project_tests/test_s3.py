import os
import tempfile

from my_meltano_project.services.s3 import get_filesystem, upload_files


def test_upload_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/test.txt", "w") as f:
            f.write("hello, world!")

        upload_files(tmpdir, root_path="/_test/")

        fs = get_filesystem()
        items = fs.ls(f"s3://{os.environ['WAREHOUSE_BUCKET']}/_test/")
        assert len(items) > 0
        fs.delete(f"s3://{os.environ['WAREHOUSE_BUCKET']}/_test/test.txt")
