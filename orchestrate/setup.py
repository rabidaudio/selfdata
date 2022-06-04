import setuptools

setuptools.setup(
    name="orchestrate",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        "dagster==0.14.17",
        "dagit==0.14.17",
        "dagster-aws==0.14.17",
        "dagster-postgres==0.14.17",
        "pytest",
    ],
)
