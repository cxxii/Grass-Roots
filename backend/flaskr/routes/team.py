from flask import request, jsonify, Blueprint
from extensions import db
from flaskr.models import Team, League


team = Blueprint("team", __name__)


# CREATE - DONE
# * DONT ALOW DUPE NAMES IN SAME LEAGUE
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
# * issue if change name and league at same time if name is dupe
@team.route("/api/v1/team/<int:team_id>/update", methods=["PUT"])
def update_team(team_id):
    team_data = Team.query.get(team_id)

    data = request.json

    if "name" in data:
        new_name = data.get("name")

        unique_name_id = Team.query.filter_by(
            name=new_name, league_id=team_data.league_id
        ).all()

        if not unique_name_id:
            team_data.name = new_name
        else:
            return jsonify({"error": "dupe team name in league"}), 500

    if "league_id" in data:
        league = League.query.get(data.get("league_id"))

        if league:
            team_data.league_id = data.get("league_id")
        else:
            return jsonify({"error": "league doesnt exist"}), 500

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


# GET ALL BY LOCATION/SPORT
# ! BUGGY
@team.route(
    "/api/v1/team/location/<string:location>/sport/<string:sport>", methods=["GET"]
)
def get_team_location(location, sport):
    leagues = League.query.filter_by(location=location, sport=sport).all()

    if leagues:
        league_ids = [league.id for league in leagues]

        teams_info = Team.query.filter(Team.league_id.in_(league_ids)).all()

        team_data = [
            {
                "id": team.id,
                "name": team.name,
                "created": team.created_at,
                "players": team.players,
                "league": team.league_id,
            }
            for team in teams_info
        ]

        return jsonify(team_data)

    return jsonify({"error": f"No teams found in {location}"}), 404
