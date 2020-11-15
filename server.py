"""Server for latin doctor search web app."""

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from model import connect_to_db, User, db
import crud
from jinja2 import StrictUndefined
import random
from geocode import geo_code
from registration import UserRegistration, UserLogIn
import os

app = Flask(__name__)  
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def homepage():
    """Search doctors by their name or specialty."""
   
    search = request.args.get("value_searched", None)  

    if search == None or search == " ":
          flash("You must provide a term to search")
          return render_template("mapform.html", doctors=[])

    doctors = db.session.execute("""
                            SELECT full_name, max(doctor_id) AS doctor_id, array_to_string(array_agg(address), ', ') AS address, array_to_string(array_agg(specialty), ', ') AS specialty FROM 
                            (SELECT doctors.full_name, doctors.doctor_id, doctors.address, specialties.specialty
                            FROM doctors
                            INNER JOIN doctors_specialties ON doctors_specialties.doctor_id = doctors.doctor_id 
                            INNER JOIN specialties ON specialties.specialty_id = doctors_specialties.specialty_id) AS D
                            WHERE D.full_name ILIKE :search OR D.specialty ILIKE :search GROUP BY full_name;""",
                            {"search": f"%{search}%"}).fetchall()

    if not doctors:
        flash("We couldn't find anything related to your search")

    return render_template("mapform.html", doctors=doctors)


@app.route('/doctor-by-specialty/<doctor_specialty>')
def get_doctors_by_specialty(doctor_specialty):
    """Return doctors by specialty from the database as JSON."""

    doctors_by_specialty = []

    if doctor_specialty == "All":
        doctors_by_specialty = crud.get_doctors()
    else:
        doctors_by_specialty = crud.get_doctors_by_specialty(doctor_specialty)
    
    for doctor in doctors_by_specialty:
        if not doctor.longitude or not doctor.latitude:
            coordinates = geo_code(doctor.address)
            doctor.longitude = coordinates['longitude']
            doctor.latitude = coordinates['latitude']
            db.session.commit()
    
    return jsonify([{
        "full_name": doctor.full_name,
        "address": doctor.address,
        "coordinates": {"longitude": doctor.longitude, "latitude": doctor.latitude}
    } for doctor in doctors_by_specialty])


@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    """Return a form for user registration."""

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = UserRegistration()
    username = form.username.data
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = crud.create_user(username, email, hashed_password) 
        flash('Account succesfully created')
        return redirect(url_for('user_login'))
 
    return render_template('registration.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Return a form for user login."""

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
  
    form = UserLogIn()
    user = User.query.filter_by(username=form.username.data).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You're logged in!")
            return redirect(url_for('homepage'))
        else:
            flash('Something went wrong! Please check your password and username and try again.')
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """Log out an User."""
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/account")
@login_required
def user_account():
    """Return user's account."""
    return render_template('account.html')


@app.route("/doctorform")
# @login_required
# werkzeug.routing.BuildError: Could not build url for endpoint 'login'. Did you mean 'user_login' instead?
def add_new_doctor_form():

    specialties = crud.get_specialties()

    name = request.form.get("fullname")
    specialty = request.form.get("doctor-specialty")
    spanish = bool(request.form.get("spanish"))
    portuguese = bool(request.form.get("portuguese"))
    address = request.form.get("doctor-specialty")

    # new_doctor = crud.add_new_doctor(name, spanish, portuguese, address)
    # new_specialty = crud.add_a_new_specialty(specialty)
    # errors
    
    return render_template('docform.html', specialties=specialties)

@app.route("/doctor/<doctor_id>", methods=["GET"])
# @login_required
def doctor(doctor_id):
    """Return profile of the given doctor."""

    docls = crud.get_doctor_by_id(doctor_id) 

    for doc in docls:
        doc_name = doc.full_name 
        doc_address = doc.address
        # why address is not working?

    if doc_name is None:
        return "Doctor not found on Database"

    
    return render_template("dprofile.html", doctor=doc_name, address=doc_address)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# import pdb
# pdb.set_trace()   

