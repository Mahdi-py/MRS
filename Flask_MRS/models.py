from Flask_MRS import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

Lists = db.Table('contains',
                 db.Column('List_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
                 db.Column('movie_id', db.String(30), db.ForeignKey('movie.id'), primary_key=True)
                 )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    lists = db.relationship('List', backref='lists', lazy=True)

    parent = db.relationship('Ratings', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    MRSRating = db.Column(db.Float, nullable=True, unique=False)

    parant = db.relationship('Ratings', backref='movie', lazy=True )

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
    movies = db.relationship('Movie', secondary=Lists, lazy='subquery',
                             backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f"List('{self.id}', '{self.name}', '{self.user_id}')"
