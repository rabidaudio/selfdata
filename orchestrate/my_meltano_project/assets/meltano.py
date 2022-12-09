from dagster import Failure, op, Array, Noneable, OpExecutionContext, AssetsDefinition, job

import subprocess

import shlex
import os
import re

def sanitize_name(name: str) -> str:
  return re.sub(r"[-]", '_', name)

# https://docs.dagster.io/concepts/assets/multi-assets

@op(config_schema={
  "blocks": Array(str),
  "env": Noneable(dict),
  "environment": Noneable(str),
  "dry-run": Noneable(bool),
  "full-refresh": Noneable(bool),
  "no-state-update": Noneable(bool),
  "force": Noneable(bool),
})
def meltano_run_op(context: OpExecutionContext) -> int:
  args = ['.meltano/run/bin']
  if context.op_config.get('environment'):
    args.append(f"--environment={context.op_config['environment']}")
  args.append('run')
  for barg in ['dry-run', 'full-refresh', 'no-state-update', 'force']:
    if context.op_config.get(barg):
      args.append(f"--{barg}")
  args = [*args, *context.op_config['blocks']]
  
  env = {
    'PATH': os.environ['PATH'],
    'MELTANO_CLI_LOG_CONFIG': 'orchestrate/dagster-logging.yml',
  }
  if context.op_config.get('env'):
    env.update(context.op_config['env'])

  cmd = shlex.join(args)
  sub_process = None
  try:
      context.log.info(f"running {cmd}")
      sub_process = subprocess.Popen(
          args=cmd,
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT,
          cwd=os.environ['MELTANO_PROJECT_ROOT'],
          env=env,
          encoding="UTF-8",
      )

      context.log.info(f"Command pid: {sub_process.pid}")

      # Stream back logs as they are emitted
      lines = []
      for line in sub_process.stdout:
          context.log.info(line.rstrip())
          lines.append(line)

      sub_process.wait()
      context.log.info("Command completed")
      if sub_process.returncode:
        raise Failure(
            description=f"Shell command execution failed: {sub_process.returncode}"
        )
      return sub_process.returncode
  finally:
      # Always terminate subprocess, including in cases where the pipeline run is terminated
      if sub_process:
          sub_process.terminate()

# Creating a job for the meltano run op is useful for testing
@job
def meltano_run():
  meltano_run_op()

def meltano_el_assets(taps, target="target-athena", **kwargs):
  return [
    AssetsDefinition.from_op(meltano_run_op.configured({"blocks": [tap, target], **kwargs}, name=sanitize_name(f"meltano_run_{tap}")))
    for tap in taps
  ]
