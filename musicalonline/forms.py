from wtforms import Form , StringField, SubmitField , PasswordField, BooleanField,IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email , EqualTo

class RegisterForm(Form):
    username = StringField("Username", validators=[InputRequired(), Length(min=5,max=20)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    button  = SubmitField("Submit")

class LoginForm(Form):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=20)])
    remember = BooleanField('Remember Me')
    button  = SubmitField("Submit")

class RecordForm(Form):
    name = StringField("Album Name", validators=[InputRequired()])
    release = IntegerField("Release", validators=[InputRequired()])
    price  = DecimalField("Price", validators=[InputRequired()])
    button = SubmitField("Submit")

class AdminLoginForm(Form):
    username = StringField("Username", validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=20)])
    button  = SubmitField("Submit")

class AdminRecordForm(Form):
    name = StringField("Album Name", validators=[InputRequired()])
    release = IntegerField("Release", validators=[InputRequired()])
    price  = DecimalField("Price", validators=[InputRequired()])
    button = SubmitField("Submit")

class TrackForm(Form):
    name = StringField("Track Name", validators=[InputRequired()])
    length = DecimalField("Length", validators=[InputRequired()])
    button = SubmitField("Submit")