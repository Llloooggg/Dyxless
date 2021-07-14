import json

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()

with open("dyxless/config.json") as config_file:
    config_data = json.load(config_file)


def create_app():
    app = Flask("__name__", template_folder="dyxless/templates")

    main_settings = config_data["main_settings"]
    app.config.update(main_settings)

    db_settings = config_data["db_settings"]
    app.config.update(db_settings)

    mail_settings = config_data["mail_settings"]
    app.config.update(mail_settings)

    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .mails import mails as mails_blueprint

    app.register_blueprint(mails_blueprint)

    return app
