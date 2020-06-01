from flask import render_template, url_for, request, flash, redirect, abort, jsonify, make_response
from Flask_MRS.forms import RegistrationForm, LoginForm, RatingForm, ListForm, NoteForm
from Flask_MRS.utils import getMovie, Search, UpdateMRSRating, MovieRatings, add_movie_to_db, getMovies
from Flask_MRS import app, db, bcrypt
from Flask_MRS.models import *
from Flask_MRS.models import lists as list_movie
from flask_login import login_user, logout_user, current_user, login_required
from json import dumps

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
@app.route('/movies/<string:id>/<string:list_id>', methods=['GET', 'POST'])
def movie_page(id, list_id=None):
    movie = getMovie(id)
    rtings = MovieRatings(UserRating=None, MRSRating=None, IMDbRating=movie['rating'])
    form = RatingForm()
    noteform = NoteForm()
    list=None
    add_movie_to_db(id)  # This function will add the movie to the data if the is not in the database
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.id))
        rtings.UserRating = Ratings.query.filter_by(movie_id=id, user_id=user.id).first()
        if rtings.UserRating is not None:
            rtings.UserRating = rtings.UserRating.rating
        rtings.MRSRating = UpdateMRSRating(id)
        if list_id:
            l=List.query.get_or_404(list_id)
            if l.user != current_user:
                abort(403)
            list= list_movie.query.filter_by(List_id=list_id, movie_id=id).first()
            noteform.note.data=list.note

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
                           MRSRating=rtings.MRSRating, form=form, list=list, noteform=noteform)

@app.route('/noteform/<string:movie_id>/<int:list_id>', methods=['post','get'])
@login_required
def noteform(movie_id, list_id):
    form = NoteForm()
    list= List.query.get(list_id)
    if list.user != current_user:
        abort(403)
    if form.validate_on_submit():
        list = list_movie.query.filter_by(List_id=list_id, movie_id=movie_id).first()
        list.note=form.note.data
        db.session.commit()
        flash('Note has been updated successfully','success')
    return redirect(url_for('movie_page',id=movie_id, list_id=list_id))

@app.route('/Lists')
@login_required
def lists():
    lists = current_user.lists
    return render_template('lists.html', lists=lists, len=len)


@app.route('/new_list', methods=['POST', 'GET'])
@login_required
def new_list():
    form = ListForm()
    if form.validate_on_submit():
        list = List(name=form.name.data, user_id=current_user.id)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('add_movie', list_id=list.id))
    return render_template('new_list.html', form=form)


@app.route('/new_list/<int:list_id>/add_movies', methods=['POST', 'GET'])
@app.route('/Lists/<int:list_id>/add_movies/<string:back>', methods=['POST', 'GET'])
@login_required
def add_movie(list_id, back=None):
    list = List.query.get_or_404(list_id)
    if list.user != current_user:
        abort(403)
    if request.method == 'POST':
        data = request.get_json()
        movie_id = data['movie_id']
        add_movie_to_db(movie_id)  # This function will add the movie to the database if it is not in the database
        movie = Movie.query.get_or_404(movie_id)
        for mov in list.movies:
            if mov == movie:
                return make_response(jsonify({"message": "exist"}), 200)
        l = list_movie(movie_id=movie_id, List_id=list_id)
        db.session.add(l)
        db.session.commit()
        return make_response(jsonify({"message": "OK"}), 200)
    return render_template('add_movies.html', list=list, back=back)


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


@app.route('/DeleteList/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_list(id):
    list = List.query.get_or_404(id)
    if list.user != current_user:
        abort(403)
    else:
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for('lists'))
    return render_template('lists.html', list=list)


@app.route('/Lists/<int:id>', methods=['POST', 'GET'])
@login_required
def list(id):
    list = List.query.get(id)
    if list.user != current_user:
        abort(403)
    movies = getMovies(list)
    return render_template('list.html', movies=movies, list_id=id, list=list)
'''
    When you go from the list to the rate page and rate the movie, it will route you to the /movies/id page 
    where it should direct the user the the /movies/id/list_id. Work it out 
'''


@app.route('/Lists/<int:list_id>/<string:movie_id>/delete')
@login_required
def delete_movie_from_list(list_id,movie_id):
    list = List.query.get(list_id)
    if list.user != current_user:
        abort(403)
    movie_in_list = list_movie.query.filter_by(List_id=list_id,movie_id=movie_id).first()
    if not movie_in_list:
        abort(404)
    db.session.delete(movie_in_list)
    db.session.commit()
    flash('Item deleted successfully','success')
    return redirect(url_for('list', id=list_id))
