from Flask_MRS import db
from datetime import datetime


movies = db.Table('ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.String(30), db.ForeignKey('movie.id'), primary_key=True),
    db.Column('rating', db.DECIMAL, nullable=False)
)

Lists = db.Table('contains',
    db.Column('List_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
    db.Column('movie_id', db.String(30), db.ForeignKey('movie.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ratings = db.relationship('Movie', secondary=movies, lazy='subquery',
        backref=db.backref('ratings', lazy=True))
    lists = db.relationship('List', backref='List', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):
    id = db.Column(db.String(30),primary_key=True)
    MRSRating = db.Column(db.DECIMAL(10), nullable=True, unique=False)


    def __repr__(self):
        return f"Movie('{self.id}', '{self.MRSRating}')"

class List(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movies = db.relationship('Movie', secondary=Lists, lazy='subquery',
                              backref=db.backref('movies', lazy=True))
    def __repr__(self):
        return f"List('{self.id}', '{self.name}', '{ self.user_id }')"