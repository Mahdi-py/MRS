import requests
import os
from Flask_MRS.models import *
from Flask_MRS import db
from flask_login import current_user

headers = {
    'x-rapidapi-host': os.environ.get('imdb_host'),
    'x-rapidapi-key': os.environ.get('imdb_key')
}


def getMovie(id):
    url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/" + id
    response = requests.request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    data = response.json()
    return data


def Search(name):
    url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/" + name
    response = requests.request("GET", url, headers=headers)
    response.encoding = 'utf-8'
    data = response.json()
    return data


def UpdateMRSRating(movie_id):
    ratings = Ratings.query.filter_by(movie_id=movie_id).all()
    sum = 0.00
    if len(ratings) != 0:
        for rating in ratings:
            sum = sum + float(rating.rating)
        rating = sum / len(ratings)
        rating = round(rating, 2)
        movie = Movie.query.filter_by(id=movie_id).first()
        movie.MRSRating = rating
        db.session.commit()
        return rating
    return None


def isfloat(num):
    try:
        num = float(num)
        return True
    except:
        return False

class MovieRatings():
    def __init__(self, UserRating, MRSRating, IMDbRating):
        self.UserRating=UserRating
        self.MRSRating=MRSRating
        self.IMDbRating=IMDbRating
    def __repr__(self):
        return 'Ratings( UserRating= '+str(self.UserRating)+", MRS Rating= "+str(self.MRSRating)+", IMDb Rating= "+str(self.IMDbRating)

def add_movie_to_db(id):
    if not Movie.query.filter_by(id=id).first():
        new_movie = Movie(id=id)
        db.session.add(new_movie)
        db.session.commit()

def getMovies(list):
    movies = []
    for movie in list.movies:
        m = getMovie(movie.movie_id)
        Rating = Ratings.query.filter_by(movie_id=movie.movie_id, user_id=list.user.id).first()
        m.update({'note': movie.note})
        m.update({'list_id': movie.List_id})
        if Rating:
            m.update({'Rating': Rating.rating})
        movies.append(m)
    return movies