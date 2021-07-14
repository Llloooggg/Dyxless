import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
        self,
        email,
        password,
        username,
        is_confirmed=False,
        is_admin=False,
    ):
        self.email = email
        self.password = generate_password_hash(password, method="sha256")
        self.username = username
        self.registered_on = datetime.datetime.now()
        self.is_confirmed = is_confirmed
        self.is_admin = is_admin
