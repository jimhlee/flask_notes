
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class CreateUserForm(FlaskForm):
    """form for adding a user"""

    username = StringField("Username",
        validators=[
        InputRequired(),
        Length(1,20,'Maxmimum length of 20 characters')])
    password = PasswordField("Password", validators=[InputRequired()])
    # wtforms has an email validator, uuse that instead
    # just remember to pip install the email validator library from wtforms
    email = StringField("Email", validators=[InputRequired()])
    # use length in the form field for first and last name too
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    '''Form for logging in'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])




class NewNoteForm(FlaskForm):
    '''form for adding a note'''
    title = StringField('title', validators=[InputRequired()])
    content = StringField('content', validators=[InputRequired()])

# below can just inherit from newnoteform in the params of editnoteform
# only need docstring
class EditNoteForm(NewNoteForm):
    '''Form to edit a note'''

    # title = StringField('title', validators=[InputRequired()])
    # content = StringField('content', validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF protection"""