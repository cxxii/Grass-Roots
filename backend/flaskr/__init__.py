from extensions import db, r, bcrypt, cors, mail
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object("config.Config")

    # Initialize Extensions
    db.init_app(app)
    r.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Routes
        from flaskr.routes import auth, league, team, player

        # Register Blueprints
        app.register_blueprint(auth.user)
        app.register_blueprint(league.league)
        app.register_blueprint(team.team)
        app.register_blueprint(player.player)

        return app
