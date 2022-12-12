# Self-data

This is a project for analyzing and reporting on behaviors from my own personal life (and my friends). Things like
media consumption, home automation, wellness, etc. Work in progress.

Currently implemented:

- Music (via Last.fm) - https://github.com/rabidaudio/tap-lastfm
- Chess (via Lichess) - https://github.com/rabidaudio/tap-lichess

Built using open-source/open-core tools, including [Meltano](https://meltano.com), [DBT](https://getdbt.com), and [Evidence](https://evidence.dev).

# Deploy

Hosted using [Meltano Cloud](https://meltano.com/cloud/)!

1. Encrypt secrets from `.env` into `secrets.yml`
2. Push code to `main`

```bash
meltano invoke kms:encrypt
git push origin main
```

# TODO

- Use evidence.dev for querying: [BLOCKED] see https://github.com/evidence-dev/evidence/pull/473 https://github.com/evidence-dev/evidence/issues/486
- sqlfluff
- integrate more sources
- make dagster utility [BLOCKED] see https://github.com/meltano/meltano/pull/6409
- switch to BATCH taps/targets on S3
- convert meltano into a cli resource
- musicbrainz dagster assets
- port listening age queries to evidence: https://github.com/rabidaudio/lfm-age-stats/blob/master/app/javascript/components/Show/index.js
- update tap-lastfm sdk version
- set up webserver for evidence assets
- save dagster runs and event logs in S3, allowing access remotely
