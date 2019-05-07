from musicalonline import app, db
from musicalonline.forms import RegisterForm, LoginForm, AdminLoginForm, AdminRecordForm, RecordForm
from musicalonline.models import User , Album
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        albums = Album.query.filter(Album.name.like("%"+request.form["search"] +"%")).all()
        return render_template("buy.html",albums=albums)
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
        if user is not None and user.password == form.password.data:
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

@app.route("/sell", methods=["GET","POST"])
def sell():
    form = RecordForm(request.form)
    if form.validate():
        album = Album(user_id=current_user.id,name=form.name.data,release=form.release.data,price=form.price.data)
        db.session.add(album)
        db.session.commit()
    return render_template("sell.html", form=form)

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    form = AdminLoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.isadmin == 1 and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("admin"))
        else:
            print("invalid")
    else:
        print("invalid")
    return render_template("adminlogin.html",form=form)

@app.route("/admin",methods=["GET"])
@login_required
def admin():
    if current_user.isadmin == 0:
        return redirect(url_for('index'))
    albums = Album.query.all()
    return render_template("admin.html", albums=albums)

@app.route("/admin/edit/<int:id>",methods=["GET","POST"])
@login_required
def admin_edit(id):
    form = AdminRecordForm(request.form)
    album = Album.query.filter_by(album_id=id).first()
    if form.validate() and album is not None:
        album.name = form.name.data
        album.release = form.release.data
        album.price = form.price.data
        db.session.commit()
    return render_template("admin_edit.html",album=album, form=form)

@app.route("/edit/<int:id>",methods=["GET","POST"])
@login_required
def edit(id):
    album = Album.query.filter_by(album_id=id).first()
    if current_user.id == album.user_id:
        form = RecordForm(request.form)
        album = Album.query.filter_by(album_id=id).first()
        if form.validate() and album is not None:
            album.name = form.name.data
            album.release = form.release.data
            album.price = form.price.data
            db.session.commit() 
    else:
        return redirect(url_for("buy"))
    return render_template("edit.html",form=form)

@app.route("/admin/delete/<int:id>")
@login_required
def admin_delete(id):
    if current_user.isadmin == 0:
        return redirect(url_for('index'))
    Album.query.filter_by(album_id=id).delete()
    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    album = Album.query.filter_by(album_id=id).first()
    if current_user.id == album.user_id:
        Album.query.filter_by(album_id=id).delete()
        db.session.commit()
        redirect(url_for("buy.html"))

@app.route("/admin/add",methods=["GET","POST"])
@login_required
def admin_add():
    if current_user.isadmin == 0:
        return redirect(url_for('index'))
    form = AdminRecordForm(request.form)
    if form.validate():
        album = Album(user_id=current_user.id,name=form.name.data,release=form.release.data,price=form.price.data)
        db.session.add(album)
        db.session.commit()
    return render_template("admin_add.html",form=form)


