from dagster import repository


@repository
def orchestrate():
    """
    The repository definition for this orchestrate Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = []
    schedules = []
    sensors = []

    return jobs + schedules + sensors
