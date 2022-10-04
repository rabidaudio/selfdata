https://developers.google.com/fit/scenarios/read-daily-step-total#rest
https://docs.aws.amazon.com/athena/latest/ug/presto-functions.html


# Deploy

```bash
heroku container:login
docker build -t selfdata .
docker tag selfdata registry.heroku.com/rabidaudio-selfdata/web
docker push registry.heroku.com/rabidaudio-selfdata/web
heroku container:release web
```
