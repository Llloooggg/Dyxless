#!/bin/bash

set echo off

export PORT=5000

docker-compose build 
docker-compose up
