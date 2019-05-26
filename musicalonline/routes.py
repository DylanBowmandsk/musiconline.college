from musicalonline import app, db
from musicalonline.forms import RegisterForm, LoginForm, AdminLoginForm, RecordForm, RecordForm, TrackForm
from musicalonline.models import User , Album, Track
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

@app.route("/buy", methods=["GET","POST"])
def buy():
    if request.method == "POST":
        albums = Album.query.filter(Album.name.like("%"+request.form["search"] +"%")).all()
        return render_template("buy.html",albums=albums)
    albums = Album.query.all()
    return render_template("buy.html", albums=albums)

@app.route("/sell", methods=["GET","POST"])
def sell():
    form = RecordForm(request.form)
    if form.validate():
        album = Album(user_id=current_user.id,name=form.name.data,release=form.release.data,price=form.price.data)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for("buy"))
    return render_template("sell.html", form=form)

@app.route("/admin/add",methods=["GET","POST"])
@login_required
def admin_add():
    if current_user.isadmin == 0:
        return redirect(url_for('index'))
    form = RecordForm(request.form)
    if form.validate():
        album = Album(user_id=current_user.id,name=form.name.data,release=form.release.data,price=form.price.data)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for("admin"))
    else:
        print("invalid")
    return render_template("admin_add.html",form=form)

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    form = AdminLoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.isadmin == 1 and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("admin"))
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
    if current_user.isadmin == 0:
        return redirect(url_for("admin"))

    #instantiate forms
    album_form = RecordForm()
    track_form = TrackForm()
    if "release" in request.form:
        print("album form")
        album_form = RecordForm(request.form)
    elif "number" in request.form:
        print("track form")
        track_form = TrackForm(request.form)
    
    # generate album and tracks
    album = Album.query.filter_by(album_id=id).first()
    tracks = album.tracks

    #filters form validation events
    if album_form.validate():
        album.name = album_form.name.data
        album.release = album_form.release.data
        album.price = album_form.price.data
        db.session.commit()
        return redirect(url_for("buy"))
    elif  track_form.validate():
        track = Track(album_id=album.album_id,track_number=track_form.number.data, name=track_form.name.data,length=track_form.length.data)
        db.session.add(track)
        db.session.commit()
        return redirect(url_for("edit",id=id))
    return render_template("admin_edit.html",album=album, album_form=album_form, track_form=track_form,  tracks=tracks)

@app.route("/edit/<int:id>",methods=["GET","POST"])
@login_required
def edit(id):
    #instantiate forms
    album_form = RecordForm()
    track_form = TrackForm()
    if "release" in request.form:
        album_form = RecordForm(request.form)
    elif "number" in request.form:
        track_form = TrackForm(request.form)

    #generate album and tracks
    album = Album.query.filter_by(album_id=id).first()
    tracks = album.tracks

    if album.user_id != current_user.id:
        return redirect(url_for("buy"))
    
    #filters form validation events
    if album_form.validate():
        album.name = album_form.name.data
        album.release = album_form.release.data
        album.price = album_form.price.data
        db.session.commit()
        return redirect(url_for("buy"))
    elif  track_form.validate():
        track = Track(album_id=album.album_id, name=track_form.name.data,length=track_form.length.data,track_number=track_form.number.data)
        db.session.add(track)
        db.session.commit()
        return redirect(url_for("edit",id=id))
    return render_template("edit.html",album=album, album_form=album_form, track_form=track_form, tracks=tracks)

@app.route("/admin/delete/album/<int:id>")
@login_required
def admin_delete(id):
    if current_user.isadmin == 0:
        return redirect(url_for('admin'))
    Album.query.filter_by(album_id=id).delete()
    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/delete/album/<int:id>")
@login_required
def delete(id):
    album = Album.query.filter_by(album_id=id).first()
    
    if  current_user.id != album.user_id:
        return redirect(url_for("buy"))

    Album.query.filter_by(album_id=id).delete()
    db.session.commit()
    return redirect(url_for("buy"))

@app.route("/admin/delete/track/<int:id>")
@login_required
def admin_track_delete(id):
    track = Track.query.filter_by(track_id=id).first()
    if current_user.isadmin == 0:
        return redirect(url_for("admin"))
    else:
        Track.query.filter_by(track_id=id).delete()
        db.session.commit()
    return redirect(url_for("buy"))

@app.route("/delete/track/<int:id>")
@login_required
def track_delete(id):
    track = Track.query.filter_by(track_id=id).first()
    if current_user.id != track.album.user_id:
        return redirect(url_for("admin"))
    else:
        Track.query.filter_by(track_id=id).delete()
        db.session.commit()
    return redirect(url_for("edit",id=track.album.album_id))
        
        


