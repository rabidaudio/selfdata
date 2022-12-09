from dagster import asset

@asset
def hello_world():
  return ["hello world"]