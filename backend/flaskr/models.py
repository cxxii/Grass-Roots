import datetime as dt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from extensions import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # CREATION
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    # PERSONAL
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    # WEB
    is_active = db.Column(
        db.Boolean, nullable=False, default=False, server_default="false"
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    # LOGIC
    league_admin = db.Column(db.Boolean(), default=False, server_default="false")
    team_admin = db.Column(db.Boolean(), default=False, server_default="false")

    # RELATIONSHIPS
    player = db.relationship("players", backref="users", lazy=True)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"


player_team = db.Table(
    "player_team",
    db.Column("player_id", db.Integer, db.ForeignKey("player.id")),
    db.Column("team_id", db.Interger, db.ForeignKey("team.id")),
)


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)

    # PERSONAL
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    display_pic = db.Column(
        db.String(255), nullable=False, default="3bc4d796a1564c70a5704ea63347efcb"
    )

    # SPORT
    position = db.Column(db.String(30), nullable=True)
    number = db.Column(db.Integer, nullable=True)
    teams = db.relationship("Team", secondary=player_team, backref="players")

    # DB
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    def __repr__(self):
        return f"<Player(first_name='{self.first_name}', last_name='{self.last_name}', sport='{self.sport}', team_name='{self.team_name}')>"


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)

    # SPORT
    sport = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    badge = db.Column(
        db.String(255), nullable=False, default="4a6d9d8630324477b3d9cd6eac485b2c"
    )
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), nullable=True)
    players = relationship("Player", backref="team", lazy=True)

    # DB
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    def __repr__(self):
        return f"<Team(sport='{self.sport}', team_name='{self.team_name}')>"


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)

    # SPORT
    name = db.Column(db.String(100), nullable=False, unique=True)
    sport = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(40), nullable=False)
    teams = relationship("Team", backref="league", lazy=True)
    logo = db.Column(
        db.String(255), nullable=False, default="dd2b0f0f465e4931b784ce9066cc5973"
    )

    # DB
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    def __repr__(self):
        return f"<League(league_name='{self.league_name}', league_sport='{self.league_sport}', location='{self.location}')>"
