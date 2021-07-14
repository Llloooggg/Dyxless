
@echo off

if not exist "db.sqlite" (
    python init_db.py
)

set FLASK_APP=dyxless
set FLASK_ENV=development

flask run