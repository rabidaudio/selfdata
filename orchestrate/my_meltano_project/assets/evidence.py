import shlex
import subprocess
from typing import List

from dagster import Failure, asset, get_dagster_logger

from my_meltano_project.services.s3 import upload_files


def _evidence_build(path):
    logger = get_dagster_logger()
    try:
        sub_process = subprocess.Popen(
            args=shlex.join(["npm", "run", "build"]),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=path,
            encoding="UTF-8",
        )
        for line in sub_process.stdout:
            logger.info(line.rstrip())

        sub_process.wait()
        if sub_process.returncode:
            raise Failure(
                description="Shell command execution failed: "
                f"{sub_process.returncode}"
            )
    finally:
        # Always terminate subprocess, including in cases where the
        # pipeline run is terminated
        if sub_process:
            sub_process.terminate()


def evidence_asset(path: str, tables: List[str], dest: str):
    @asset(
        non_argument_deps={f"sqlite_tmp_{table}" for table in tables}, name="evidence"
    )
    def evidence():
        _evidence_build(path)
        upload_files(f"{path}/build", root_path=dest)

    return evidence
