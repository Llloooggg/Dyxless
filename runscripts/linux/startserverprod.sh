#!/bin/bash

set echo off

export FLASK_APP=dyxless
export FLASK_ENV=development

gunicorn --bind 0.0.0.0:5000 dyxless.__init__:app
