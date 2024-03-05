from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class CreateUserForm(FlaskForm):
    """form for adding a user"""

    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    '''Form for logging in'''

    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF protection"""