"""Models for doctor search app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Doctor(db.Model):
    """A doctor."""

    __tablename__ = 'doctors'

    doctor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    spanish = db.Column(db.Boolean(), nullable=False)
    portuguese = db.Column(db.Boolean(), nullable=False)
    address = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.String(80))
    latitude = db.Column(db.String(80))


    def __repr__(self):
        return f'Doctor name: {self.full_name}.'


class Specialty(db.Model):
    """A specialty"""

    __tablename__ = 'specialties'

    specialty_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    specialty = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'Specialty : {self.specialty}.'


class DoctorSpecialty(db.Model):
    """The doctor's specialty."""

    __tablename__ = 'doctors_specialties'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), primary_key=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.specialty_id'), primary_key=True)
    
    doctor = db.relationship('Doctor', backref='doctors_specialties')
    specialty = db.relationship('Specialty', backref='doctors_specialties')

    def __repr__(self):
        return f'Doctor ID: {self.doctor.full_name}, specialty ID: {self.specialty.specialty}.'

class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def get_id(self):
        return str(self.user_id)


    # review = db.relationship('Review', backref='users')

    def __repr__(self):
        return f'User: {self.username}, email:{self.email}'

class Review(db.Model):
    """A review written by an user"""

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    review_content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.review_content}' 
 
class Favorite(db.Model):
    
    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)


def connect_to_db(flask_app, db_uri='postgresql:///medical', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
