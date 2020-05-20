from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from Flask_MRS.models import *
from Flask_MRS.utils import isfloat

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):  # to check the data from the form with the data in the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The user name is taken. Please choose a different one.')

    def validate_email(self, email):
        email1 = User.query.filter_by(email=email.data).first()
        if email1:
            raise ValidationError('The email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class RatingForm(FlaskForm):
    rate = StringField('Yours', validators=[DataRequired()])
    submit = SubmitField('Rate')
    def validate_rate(self,rate):
        if rate.data == "None":
            raise ValidationError('You haven\'t rate it yet')
        elif not isfloat(rate.data):
            raise ValidationError('The entered data is not a number')
        elif float(rate.data) < 0 or float(rate.data) > 10:
            raise ValidationError('The number must be between 0 and 10')