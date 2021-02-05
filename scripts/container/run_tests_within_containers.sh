#!/usr/bin/env bash

for service in $(docker-compose ps --service); do
    echo "$service"
    docker-compose exec "$service" scripts/run_test.sh
done
