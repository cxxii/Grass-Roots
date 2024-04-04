from flask import Flask
from extensions import db, r, bcrypt, cors


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('config.Config')

    # Initialize Extensions
    db.init_app(app)
    r.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():

        # Routes
        from flaskr.routes import auth

        return app
