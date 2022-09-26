Currently using `yoyo-postgres:apply-setup` for `CREATE SCHEMA ...` migrations
and `yoyo-postgres:apply-postrun` for adding indexes.
Both could be done with custom utility plugins in the future, which would be pretty neat.

https://developers.google.com/fit/scenarios/read-daily-step-total#rest


# Deploy

```bash
kubectl config use-context selfdata
# kubectl edit secrets meltano_secrets
HOST=541780455112.dkr.ecr.us-east-1.amazonaws.com
REPO=$HOST/selfdata
TAG=$(git rev-parse --short HEAD)
docker login -u AWS -p $(aws ecr get-login-password) https://$HOST
docker build -t $REPO:$TAG .
docker push $REPO:$TAG
docker tag $REPO:$TAG $REPO:latest
docker push $REPO:latest
kubectl rollout restart deployment selfdata
```
