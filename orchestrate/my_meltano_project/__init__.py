from dagster import materialize

from .repository import my_meltano_project

if __name__ == "__main__":
    materialize(my_meltano_project)
