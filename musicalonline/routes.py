from musicalonline import app, db
from musicalonline.forms import RegisterForm, LoginForm
from musicalonline.models import User , Album
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm(request.form)
    if form.validate():
        user = User(username=form.username.data, email=form.email.data,password=form.password.data,isadmin=0)
        db.session.add(user)
        db.session.commit()
        print("true")
    else:
        print("not valid")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            login_user(user, remember=form.remember.data)
            print("user " + user.username + " logged in")
            return redirect(url_for("index"))
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    print("logged out")
    return redirect(url_for("index"))

@app.route("/buy")
def buy():
    albums = Album.query.all()
    return render_template("buy.html", albums=albums)
