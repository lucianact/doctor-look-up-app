from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import User
from crud import check_username, check_email

class UserRegistration(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password')])
    submit_button = SubmitField('Sing up') 

    def validate_username(self, username):
        
        username = username.data
        user = check_username(username)
        if user:
            raise ValidationError ('That username is alredy taken')
    
    def validate_email(self, email):

        email = email.data
        user = check_email(email)
        if user:
            raise ValidationError ('That email is alredy taken')
 
class UserLogIn(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember_me = BooleanField('Remember me')
    submit_button = SubmitField('Log in')
 
