import os
import shlex
import subprocess

from dagster import Failure, asset, get_dagster_logger


@asset(
    non_argument_deps={
        "sqlite_listens_per_month",
        "sqlite_lastfm_users",
        "sqlite_chess_outcomes_by_month",
        "sqlite_chess_openings",
    }
)
def evidence_docs():
    logger = get_dagster_logger()
    try:
        sub_process = subprocess.Popen(
            args=shlex.join(["npm", "run", "build"]),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=f"{os.environ['MELTANO_PROJECT_ROOT']}/notebook",
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
