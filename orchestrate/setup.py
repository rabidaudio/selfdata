from setuptools import find_packages, setup

setup(
    name="my_meltano_project",
    packages=find_packages(exclude=["my_meltano_project_tests"]),
    install_requires=[
        "dagster",
    ],
    extras_require={
        "dev": [
            "dagit",
            "pytest",
        ]
    },
)
