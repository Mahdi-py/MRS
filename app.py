from flask import Flask, request
from flask import render_template, url_for
from forms import RegistrationForm, LoginForm
from utils import getMovie, Search

app = Flask(__name__)

movie = [
    {
        'title':'Inception',
        'image':'..static/inception.jpg'
    },
    {
        'title':'Inception',
        'image':'..static/inception.jpg'
    },
    {
        'title':'Inception',
        'image':'..static/inception.jpg'
    }
]


@app.route('/')
@app.route('/index')
def home():

    return render_template('home.html', title='Home', movies=movie)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/movies/<string:id>')
def movie_page(id):
    return render_template('movie_page.html')

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method=='POST':
        name = request.form['search']
        movies = Search(name)['titles']
    return render_template('search.html', movies=movies)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
