from flask import request, jsonify, make_response, current_app, Blueprint
import email_validator
from flask_mail import Message
from extensions import bcrypt, db, mail
from flaskr.models import User
import jwt
import datetime as dt
from datetime import timezone

user = Blueprint("user", __name__)

"""
* TODO
* retoken the user if expired
* forgot password
* change password
"""


@user.route("/api/v1/signup", methods=["POST"])
def signup():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    try:
        email_validator.validate_email(email)
    except email_validator.EmailNotValidError:
        return jsonify({"message": "Invalid email"}), 401

    user = User.query.filter_by(email=email).first()

    if user is None:
        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode(
            {
                "user": new_user.id,
                "exp": dt.datetime.now(timezone.utc) + dt.timedelta(minutes=15),
            },
            current_app.config["SECRET_KEY"],
        )

        new_user.reg_token = token
        db.session.commit()

        email_token(email, token)

        current_app.logger.info(f"Registration: {email} : {token}")

        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "Email already registered"}), 409


@user.route("/api/v1/user/verifyEmail", methods=["GET"])
def confirm_email():
    reg_email = request.args.get("email")
    token = request.args.get("token")

    user = User.query.filter_by(email=reg_email).first()

    if user is None:
        return jsonify({"message": "User not found"}), 200

    try:
        jwt.decode(
            user.reg_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401

    if user.reg_token != token:
        return jsonify({"message": "Invalid token"}), 401

    if user.is_active:
        return jsonify({"message": "User is already active"}), 200

    user.is_active = True
    db.session.commit()

    return jsonify({"message": "User activation successful"}), 200


@user.route("/api/v1/login", methods=["POST"])
def login():
    auth = request.authorization

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response("Email not found", 401)

    if not bcrypt.check_password_hash(user.password, auth.password):
        return make_response(
            "Incorrect password!",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    if user.is_active:  # continue with login
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": dt.datetime.now(timezone.utc) + dt.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
        )
        current_app.logger.info(f"Registration: {user} : {token}")

        return "log in token for auth pages"

    else:
        return jsonify({"message": "user not active - check email"})


@user.route("/api/v1")
def index():
    return "index"


def email_token(email, token):
    msg = Message("CONFIRM YOUR EMAIL",
                  sender="from@example.com",
                  recipients=[email])

    msg.html = f'<p>Please confirm email by clicking the link below</p><a href="http://localhost:5000/api/v1/user/verifyEmail?email={email}&token={token}">click here</a>'
    mail.send(msg)