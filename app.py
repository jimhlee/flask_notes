import os

from flask import Flask, redirect, render_template, session, flash

from models import db, connect_db, User
from forms import CreateUserForm, LoginForm, CSRFProtectForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_homepage():
    """redirect to /register"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def show_and_process_register_user_form():
    """get and process user registration form"""

    form = CreateUserForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        # TODO: emails = User.query(User.email) how to do this?
        new_user = User.register(**data)
        # session add in model(register), session commit in view function
        # provides opportunity to add elsewhere in view function if necessary
        # and only commit once. each method should add, view function commits
        db.session.add(new_user)
        db.session.commit()
        # make user_id a global constant, allows for one change instead of many
        # changes and prevents typos
        session['user_id'] = new_user.username

        flash("User added.")
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("user_register_form.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Logs in user if successful and returns login page if unsuccessful '''
    form = LoginForm()

    if form.validate_on_submit():
        username= form.username.data
        password= form.password.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = username
            # redirect to user/username instead. right now leads to login url instead
            return render_template('user_info.html', user=user)
    # else block should be related to if user block above
    else:
        form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def show_user_info(username):
    """show user info for logged-in users only"""
    # use the username var passed in on show_user_info instead of querying db
    # only query db on success
    user = User.query.get_or_404(username)
    # is there a username in the session at all? if not below raises key error
    # raise error here unauthorized from werkzeug instead of redirected
    if session["user_id"] != user.username:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        return render_template("user_info.html", user=user)


@app.post("/logout")
def logout_user():
    """log out user"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("user_id", None)

    return redirect("/")