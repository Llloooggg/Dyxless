set echo off

export FLASK_APP=dyxless

flask db init
flask db migrate
flask db upgrade
