#!/usr/bin/env bash

docker-compose up -d
for service in $(docker-compose ps --service); do
    echo "$service"
    docker-compose exec "$service" scripts/prepare_environment.sh
done
