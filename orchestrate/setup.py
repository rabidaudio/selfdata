from setuptools import find_packages, setup

setup(
    name="my_meltano_project",
    packages=find_packages(exclude=["my_meltano_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-dbt",
        "dbt-core~=1.3.0",
        "dbt-athena-community~=1.3.0",
    ],
    extras_require={
        "dev": [
            "dagit",
            "pytest",
            "tox",
        ]
    },
)
