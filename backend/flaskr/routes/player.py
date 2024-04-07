from flask import request, jsonify, Blueprint
from extensions import db
from flaskr.models import Player


player = Blueprint("player", __name__)


# CREATE
@player.route("/api/v1/player/create", methods=["POST"])
def create_player():
    data = request.json

    first = data.get("first")
    last = data.get("last")
    position = data.get("position")
    pic = data.get("pict")
    number = data.get("number")
    user = data.get("user")

    if not first:
        return jsonify({"error": "Name is required"}), 400

    new_player = Player(
        first_name=first,
        last_name=last,
        display_pic=pic,
        position=position,
        number=number,
        user_id=user,
    )

    try:
        db.session.add(new_player)
        db.session.commit()

        return jsonify({"message": "Player created successfully"}), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500
