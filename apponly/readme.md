for testing purposes, follow worker's readme first

cd into this directory

docker build -t walkoff/walkoff-app .

docker run --name walkoff-app -dit --network devnet --ip="172.18.0.3" --entrypoint=/bin/bash walkoff/walkoff-app

docker exec -it walkoff-app /bin/bash

export WALKOFF_DB_USERNAME=walkoff
export WALKOFF_DB_PASSWORD=walkoff

when ready to start flask app:

python walkoff.py -a -c data/walkoff.config

navigate to 172.18.0.3:5000