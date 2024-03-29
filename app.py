import os

from flask import Flask, redirect, render_template, session, flash

from models import db, connect_db, User, Note
from forms import CreateUserForm, LoginForm, CSRFProtectForm, NewNoteForm, EditNoteForm

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

    # is there a username in the session at all? if not below raises key error
    # raise error here unauthorized from werkzeug instead of redirected
    if session["user_id"] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        user = User.query.get_or_404(username)
        # user.notes already has the notes, it can be accessed inside the html template
        notes = Note.query.filter(Note.owner_username == username)
        return render_template("user_info.html", user=user, notes=notes)


@app.post("/logout")
def logout_user():
    """log out user"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("user_id", None)

    return redirect("/")


@app.post("/users/<username>/delete")
def remove_user(username):
    """delete notes and user, redirect to root route"""

    notes = Note.query.filter(Note.owner_username == username)

    for note in notes:
        db.session.delete(note)
    # first commit is not necessary, handled all in 110
    db.session.commit()
    db.session.delete(username)
    db.session.commit()

    return redirect("/")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def display_notes_form(username):
    """add new note"""
    # check with session for username here as well before everything else

    form = NewNoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content, owner_username=username)

        db.session.add(new_note)
        db.session.commit()
        # move below line above validate on submit, no need to actually use value
        user = User.query.get_or_404(username)
        return redirect(f"/users/{username}")

    else:
        return render_template("notes_add_form.html", form=form)

@app.route('/notes/<int:id>/update', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)

    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{note.owner_username}')
    else:
        render_template('notes_edit_form.html', form=form)

# use int:id below in route
@app.post('/notes/<id>/delete')
def delete_post(id):
    note = Note.query.get_or_404(id)
    # user = User.query.get_or_404(note.owner_username)
    # use CSRF protection even here
    db.session.delete(note)
    db.session.commit()

    # return redirect(f'/users/{note.owner_username}', user=user)
    return redirect(f'/users/{note.owner_username}')