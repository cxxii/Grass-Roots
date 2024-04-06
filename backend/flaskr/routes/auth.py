from flask import request, jsonify, make_response, current_app, Blueprint
from extensions import bcrypt, db
from flaskr.models import User
import jwt
import datetime as dt
from datetime import timezone

user = Blueprint("user", __name__)


@user.route("/api/v1/signup", methods=["POST"])
def signup():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User.query.filter_by(email=email).first()

    if user is None:
        new_user = User(email=email, password=hashed_password)

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

        current_app.logger.info(f"Registration: {email} : {token}")

        return jsonify({"message": "User created successfully", "token": token}), 201
    return jsonify({"message": "Email already registered"}), 409
