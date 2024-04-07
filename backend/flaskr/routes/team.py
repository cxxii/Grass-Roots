from flask import request, jsonify, Blueprint
from extensions import db
from flaskr.models import Team


team = Blueprint("team", __name__)

# CREATE - DONE
@team.route("/api/v1/team/create", methods=["POST"])
def create_team():
    data = request.json
    name = data.get("name")
    league_id = data.get("league")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_team = Team(name=name, league_id=league_id)

    try:
        db.session.add(new_team)
        db.session.commit()

        return jsonify({"message": "Team created successfully"}), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# DELETE - DONE
@team.route("/api/v1/team/<int:team_id>/delete", methods=["DELETE"])
def delete_team(team_id):
    team_data = Team.query.get(team_id)

    if not team_data:
        return jsonify({"error": "Team not found"}), 404

    try:
        db.session.delete(team_data)
        db.session.commit()

        return jsonify({"message": "Team deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# UPDATE - DONE
@team.route("/api/v1/team/<int:team_id>/update", methods=["PUT"])
def update_team(team_id):
    team_data = Team.query.get(team_id)

    data = request.json

    if "sport" in data:
        team_data.sport = data.get("sport")

    if "name" in data:
        team_data.team_name = data.get("team_name")

    if "league_id" in data:
        team_data.sport = data.get("league_id")

    try:
        db.session.commit()

        return jsonify({"message": "Team updated successfully"}), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"error": str(e)}), 500


# GET ALL - DONE
@team.route("/api/v1/team/all", methods=["GET"])
def get_team():
    teams = Team.query.all()

    if not teams:
        return jsonify({"error": "No teams found"}), 404

    team_data = [
        {
            "id": team.id,
            "team_name": team.team_name,
            "team_sport": team.sport,
            "league_id": team.league_id,
            "created": team.created_at,
            "player": team.players,
        }
        for team in teams
    ]

    return jsonify(team_data), 200


# GET SINGLE - DONE
@team.route("/api/v1/team/<int:team_id>", methods=["GET"])
def single_team(team_id):
    team = Team.query.get(team_id)

    team = [
        {
            "id": team.id,
            "team_name": team.name,
            "league_id": team.league_id,
            "created": team.created_at,
            "players": team.players,
        }
    ]

    if not team:
        return jsonify({"error": "Team not found"}), 404
    else:
        return jsonify(team), 200
