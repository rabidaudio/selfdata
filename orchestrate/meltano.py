import os
import json
import subprocess

import dagster
from dagster import (
  Array,
  Noneable,
)

import dagster_shell


# Dagster is particular about naming conventions
def sanitize_name(name):
  return name.replace(".", "_").replace("-", "_")

def execute(*args, **kwargs):
  output, returncode = dagster_shell.utils.execute(*args, **kwargs)
  if returncode:
    raise dagster.Failure(f"Shell command execution failed: {returncode}")

  return output

class LogConverter:
  def __init__(self, context) -> None:
    self.context = context
  
  def info(self, message):
    try:
      data = json.loads(message)
      level = data.get('level', 'info')
      self.context.log.log(level, data['event'])
    except json.decoder.JSONDecodeError:
      self.context.log.info(message)


project_root = os.getenv("MELTANO_PROJECT_ROOT")

timezone = os.getenv("DAGSTER_SCHEDULE_TIMEZONE")

@dagster.op(
  config_schema={
    "blocks": Array(str),
    "env": Noneable(dict),
    "full-refresh": Noneable(bool),
    "force": Noneable(bool),
    "dry-run": Noneable(bool),
    "environment": Noneable(str),
  }
)
def meltano_run(context):
  """Invoke `meltano run` with the provided args."""
  args = []
  if context.solid_config.get("environment"):
    args.append(f"--environment {context.solid_config['environment']}")
  args.append('run')
  if context.solid_config.get('dry-run'):
    args.append("--dry-run")
  if context.solid_config.get('full-refresh'):
    args.append("--full-refresh")
  if context.solid_config.get('force'):
    args.append("--force")

  cmd =  " ".join([
    ".meltano/run/bin",
    *args,
    *context.solid_config["blocks"],
  ])

  env = {}
  env.update(os.environ)
  env['MELTANO_CLI_LOG_CONFIG'] = "orchestrate/dagster-logging.yml"
  if context.solid_config["env"]:
    env.update(context.solid_config["env"])

  execute(
    cmd,
    output_logging="STREAM",
    log=LogConverter(context),
    env=env,
    cwd=project_root,
  )

@dagster.repository
def meltano_pipelines():
  """Return all the pipelines and schedules for our Meltano project.

  It creates a pipeline to run each job referenced by a schedule.
  """
  result = subprocess.run(
    [".meltano/run/bin", "schedule", "list", "--format=json"],
    cwd=project_root,
    stdout=subprocess.PIPE,
    universal_newlines=True,
    check=True,
  )
  configs = json.loads(result.stdout)

  jobs = []
  schedules = []

  # NOTE: old "elt" schedules from Meltano V1 are ignored
  for config in configs['schedules']['job']:
    name = sanitize_name(f"meltano_{config['name']}")

    @dagster.job(
      name=name,
      config={
        "ops": {
          "meltano_run": {
            "config": {
              "env": config["env"],
              "blocks": [config['job']['name']],
            }
          }
        }
      }
    )
    def _meltano_job():
      meltano_run()
    
    jobs.append(_meltano_job)

    if config["cron_interval"]:
      schedule = dagster.ScheduleDefinition(
          name=f"{name}_schedule",
          cron_schedule=config["cron_interval"],
          job=_meltano_job,
          execution_timezone=timezone,
      )
      schedules.append(schedule)

    return [*jobs, *schedules]
