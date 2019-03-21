from musicalonline import app, db
from musicalonline.forms import RegisterForm, LoginForm
from musicalonline.models import User
from flask import render_template, request


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        user = User(username=form.username.data, email=form.email.data,password=form.password.data,isadmin=0)
        db.session.add(user)
        db.session.commit()
        print("true")
    else:
        print("not valid")
    return render_template("register.html", form=form)

@app.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("login.html",form=form)