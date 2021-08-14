import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    Markup,
)
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

from . import db
from .models import User
from .mails import send_async_email

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    elif request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Неверный логин или пароль", "is-danger")
            return redirect(url_for("auth.login"))
        elif not user.is_confirmed:
            flash(
                "Аккаунт еще не активирован. Пожалуйста, проверьте вашу почту",
                "is-warning",
            )
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)

        user.last_login = datetime.datetime.now()

        db.session.commit()

        return redirect(url_for("main.profile"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    elif request.method == "GET":
        return render_template("signup.html")

    elif request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            login_url = url_for("auth.login")
            flash(
                Markup(
                    f"Указанная почта уже используется.<br><a href='{login_url}'>Перейти к странице входа</a>"
                ),
                "is-danger",
            )
            return redirect(url_for("auth.signup"))

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Указанное имя уже используется", "is-danger")
            return redirect(url_for("auth.signup"))

        new_user = User(
            email=email,
            password=password,
            username=username,
        )

        db.session.add(new_user)
        db.session.commit()

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for(
            "auth.confirm_email", token=token, _external=True
        )

        send_async_email(
            subject="Подтверждение регистрации",
            recipients=[new_user.email],
            html=render_template(
                "mail/confirmation_mail.html", confirm_url=confirm_url
            ),
        )

        flash(
            "На вашу почту была выслана ссылка для подтверждения регистрации",
            "is-success",
        )

        return redirect(url_for("auth.login"))


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(
        email, salt=current_app.config["SECURITY_PASSWORD_SALT"]
    )


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration,
        )
    except:
        return False
    return email


@auth.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("Ссылка подтверждения невалидна или устарела", "is-danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash("Аккаунт уже подтвержден", "is-success")
    else:
        user.is_confirmed = True
        db.session.commit()
        flash("Ваш аккаунт подвтержден!", "is-success")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
