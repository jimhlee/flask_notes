from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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



def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)