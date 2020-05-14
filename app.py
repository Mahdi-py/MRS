from flask import Flask
from flask import render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html', title='Home')


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


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
