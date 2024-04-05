import datetime as dt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from extensions import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    is_active = db.Column(
        db.Boolean, nullable=False, default=False, server_default="false"
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    site_admin = db.Column(db.Boolean(), default=False)
    league_admin = db.Column(db.Boolean(), default=False)
    team_admin = db.Column(db.Boolean(), default=False)

    player = db.relationship('players', backref='users', lazy=True)

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