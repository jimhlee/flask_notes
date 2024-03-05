import os

from flask import Flask, redirect, render_template, session, flash

from models import db, connect_db, User
from forms import CreateUserForm, LoginForm

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
def show_and_process_register_user_form():
    """get and process user registration form"""

    form = CreateUserForm()
    username = form.username.data


    if form.validate_on_submit():
        # session['user_id'] = username
        # db.session.add(username)
        # db.session.commit()
        # return redirect(f"/users/{form.username.data}")
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.username

        flash("User added.")
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("user_register_form.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Logs in user  if successful '''

    form = LoginForm()

    if form.validate_on_submit():
        username= form.username.data
        password= form.password.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = username
            return redirect('/')

    else:
        form.username.errors = ["Bad name/password"]

    # TODO: need to create login html
    return render_template("login.html", form=form)

# user = User.query.get_or_404(user.username)