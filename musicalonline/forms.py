from wtforms import Form , StringField, SubmitField , PasswordField, BooleanField
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