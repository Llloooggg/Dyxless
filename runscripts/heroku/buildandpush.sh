#!/bin/bash

docker-compose build
heroku container:push web -a dyxless || true
heroku container:release web -a dyxless
