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
