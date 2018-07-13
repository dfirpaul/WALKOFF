for testing purposes -- follow this before app's readme

cd into this directory

docker build -t walkoff/walkoff-worker .

docker network create --driver=bridge --subnet=172.18.0.0/24 devnet

docker pull redis
docker run --name walkoff-redis -d --network devnet --ip="172.18.0.2" redis

docker pull postgres
docker run --name walkoff-postgres -e POSTGRES_USER=walkoff -e POSTGRES_PASSWORD=walkoff --network devnet --ip='172.18.0.5' -d postgres

docker run --name walkoff-worker -dit --network devnet --ip="172.18.0.3" --entrypoint=/bin/bash walkoff/walkoff-worker

docker exec -it walkoff-worker /bin/bash

export WALKOFF_DB_USERNAME=walkoff
export WALKOFF_DB_PASSWORD=walkoff


when ready to start workers:

python start_workers.py -c data/walkoff.config
