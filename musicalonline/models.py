from musicalonline import db
from musicalonline import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    isadmin = db.Column(db.Integer, nullable=False)
    albums = db.relationship("Album", backref="author", lazy=True)

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(80) , unique=False, nullable=False)
    release = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    tracks = db.relationship("Track", backref="album", lazy=True,order_by='Track.track_number.asc()')

class Track(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.album_id"), nullable=False)
    track_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    length = db.Column(db.Float, nullable=False)






