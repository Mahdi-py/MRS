from flask import render_template, url_for, request, flash, redirect
from Flask_MRS.forms import RegistrationForm, LoginForm, RatingForm
from Flask_MRS.models import Ratings
from Flask_MRS.utils import getMovie, Search, UpdateMRSRating, MovieRatings
from Flask_MRS import app, db, bcrypt
from Flask_MRS.models import *
from flask_login import login_user, logout_user, current_user, login_required

movie = [
    {
        'title': 'Inception',
        'image': '..static/inception.jpg'
    },
    {
        'title': 'Inception',
        'image': '..static/inception.jpg'
    },
    {
        'title': 'Inception',
        'image': '..static/inception.jpg'
    }
]


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html', title='Home', movies=movie)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for your registration. Please Login now ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data) and user:
            login_user(user, remember=form.remember.data)
            flash('You are logged in successfully', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Password or username is incorrect !!', 'info')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/movies/<string:id>', methods=['GET', 'POST'])
def movie_page(id):
    movie = getMovie(id)
    rtings = MovieRatings(UserRating=None, MRSRating=None, IMDbRating=movie['rating'])
    form = RatingForm()
    if not Movie.query.filter_by(id=id).first():
        new_movie = Movie(id=id)
        db.session.add(new_movie)
        db.session.commit()
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.id))
        rtings.UserRating = Ratings.query.filter_by(movie_id=id, user_id=user.id).first().rating
        rtings.MRSRating = UpdateMRSRating(id)
    if form.validate_on_submit():
        Rating = form.rate.data
        rating = Ratings.query.filter_by(user_id=current_user.id, movie_id=id).first()
        if not rating:
            new_rating = Ratings(user_id=current_user.id, movie_id=id, rating=round(float(Rating), 2))
            db.session.add(new_rating)
            db.session.commit()
            rtings.UserRating = new_rating.rating
        else:
            rating.rating = round(float(Rating), 2)
            db.session.commit()
            rtings.UserRating = round(float(Rating), 2)
    return render_template('movie_page.html', movie=movie, Rating=rtings.UserRating,
                           MRSRating=rtings.MRSRating, form=form)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        name = request.args.get('search')
        movies = Search(name)
        error = False
        try:
            movies['message']
            error = True
        except:
            _ = 'nothing'
    return render_template('search.html', movies=movies, error=error)
