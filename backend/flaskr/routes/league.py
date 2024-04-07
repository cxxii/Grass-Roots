from flask import request, jsonify, Blueprint
from extensions import db
from flaskr.models import League


league = Blueprint("league", __name__)


# CREATE
@league.route("/api/v1/league/create", methods=["POST"])
def create_league():
    data = request.json
    name = data.get("name")
    sport = data.get("sport")
    location = data.get("location")

    required_fields = {
        "name": "League name",
        "sport": "Sport",
        "location": "League location",
    }

    for field, display_name in required_fields.items():
        if not request.json.get(field):
            return jsonify({"error": f"{display_name} required"}), 400

    new_league = League(name=name, sport=sport, location=location)

    try:
        db.session.add(new_league)
        db.session.commit()

        return jsonify({"message": "League created successfully"}), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# DELETE
@league.route("/api/v1/league/<int:league_id>/delete", methods=["DELETE"])
def delete_league(league_id):
    league_data = League.query.get(league_id)

    if not league_data:
        return jsonify({"error": "league not found"}), 404

    try:
        db.session.delete(league_data)
        db.session.commit()

        return jsonify({"message": "league deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# GET ALL
@league.route("/api/v1/league/all", methods=["GET"])
def get_league():
    leagues = League.query.all()

    if not leagues:
        return jsonify({"error": "No leagues found"}), 404

    return jsonify(league_data_dict(leagues))


# GET ALL BY SPORT
@league.route("/api/v1/league/<string:sport>", methods=["GET"])
def get_league_sport(sport):
    leagues = League.query.filter_by(sport=sport).all()

    if leagues:
        return jsonify(league_data_dict(leagues))

    return jsonify({"error": f"No {sport} leagues found"}), 404


@league.route("/api/v1/league/<string:location>", methods=["GET"])
def get_league_location(location):
    leagues = League.query.filter_by(location=location).all()

    if leagues:
        return jsonify(league_data_dict(leagues))

    return jsonify({"error": f"No {location} leagues found"}), 404


# GET ALL BY SPORT & LOCATION
@league.route("/api/v1/league/<string:location>/<string:sport>", methods=["GET"])
def get_league_sportlocation(sport, location):
    leagues = League.query.filter_by(sport=sport, location=location).all()

    if leagues:
        return jsonify(league_data_dict(leagues))

    return jsonify({"error": f"No {sport} leagues found"}), 404


# GET SINGLE
@league.route("/api/v1/league/<int:league_id>", methods=["GET"])
def get_league_id(league_id):
    league = League.query.get(league_id)

    if league:
        return jsonify({
            "id": league.id,
            "name": league.name,
            "sport": league.sport,
            "location": league.location,
            "created_at": league.created_at
        })
    else:

        return jsonify({"error": f"No league found with ID {league_id}"}), 404


# UPDATE
@league.route("/api/v1/league/<int:league_id>/update", methods=["PUT"])
def update_league(league_id):
    league_data = League.query.get(league_id)

    data = request.json

    if "league_name" in data:
        league_data.league_name = data.get("league_name")

    if "league_sport" in data:
        league_data.league_sport = data.get("league_sport")

    if "location" in data:
        league_data.location = data.get("location")

    try:
        db.session.commit()

        return jsonify({"message": "League updated successfully"}), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


def league_data_dict(leagues):

    league_data = [
        {
            "id": league.id,
            "league_name": league.name,
            "league_sport": league.sport,
            "location": league.location,
            "created": league.created_at,
        }
        for league in leagues
    ]

    return league_data