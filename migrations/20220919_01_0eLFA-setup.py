"""
setup
"""

from yoyo import step

__depends__ = {'20220612_02_ewdWO-postrun'}

steps = [
    step("CREATE SCHEMA IF NOT EXISTS tap_lichess")
]
