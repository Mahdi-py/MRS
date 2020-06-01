from Flask_MRS import db, login_manager, manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class lists(db.Model):
    List_id = db.Column(db.Integer, db.ForeignKey('list.id'), primary_key=True)
    movie_id = db.Column(db.String(30), db.ForeignKey('movie.id'), primary_key=True)
    note = db.Column(db.String(1000), nullable=True, unique=False)

    child = db.relationship('List', backref='movies', lazy=True)
    parent = db.relationship('Movie', backref='lists', lazy=True)

    def __repr__(self):
        return f"list_movie(List='{self.List_id}', Movie='{self.movie_id}', note='{self.note}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    child = db.relationship('List', backref='user', lazy=True)
    parent = db.relationship('Ratings', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    MRSRating = db.Column(db.Float, nullable=True, unique=False)

    parant = db.relationship('Ratings', backref='movie', lazy=True)
    child = db.relationship('lists', backref='movie', lazy=True, cascade="all,delete")

#    movies = db.relationship('List', secondary=lists, lazy='subquery',
#                             backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f"Movie('{self.id}', '{self.MRSRating}')"


class Ratings(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.String(30), db.ForeignKey('movie.id'), primary_key=True)
    rating = db.Column(db.Float, nullable=False)

    child = db.relationship('Movie', backref='ratings', lazy=True)
    parent = db.relationship('User', backref='ratings', lazy=True)

    def __repr__(self):
        return f"Rating('{self.user_id}', '{self.movie_id}', '{self.rating}')"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    parant = db.relationship('User', backref='lists', lazy=True)
    child = db.relationship('lists', backref='list', lazy=True, cascade="all,delete")


    def __repr__(self):
        return f"List('{self.id}', '{self.name}', '{self.user_id}')"
