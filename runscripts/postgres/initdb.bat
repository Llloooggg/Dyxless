
@echo off

set FLASK_APP=dyxless

flask db init
flask db migrate
flask db upgrade
