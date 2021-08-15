
@echo off

set FLASK_APP=dyxless

gunicorn --bind 0.0.0.0:$PORT dyxless.__init__:app
