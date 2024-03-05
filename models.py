from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    '''User'''
    __tablename__ = 'users'

    username = db.Column(
        db.String(20),
        primary_key = True,
        nullable = False
    )

    hashed_password = db.Column(
        db.String(100),
        nullable = False
    )

    email = db.Column(
        db.String(50),
        nullable = False,
        unique = True
    )

    first_name = db.Column(
        db.String(30),
        nullable = False
    )

    last_name = db.Column(
        db.String(30),
        nullable = False
    )

    @classmethod
    def register(cls, username, pwd):
        """register user w/ hashed password & return user"""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, pwd):
        """validate that user exists and password is correct"""

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False



def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)