"""
Add schema for lastfm.
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE SCHEMA IF NOT EXISTS tap_lastfm")
]
