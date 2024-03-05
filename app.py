import os

from flask import Flask, redirect, render_template

from models import db, connect_db, User
from forms import CreateUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


@app.get("/")
def redirect_to_homepage():
    """redirect to /register"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def show_and_process_user_form():
    """get and process user form"""

    user = User.query.all()
    form = CreateUserForm()

    if form.validate_on_submit():


        return redirect("/users/<username>")

    else:
        return render_template("user_register_form.html", form=form)
