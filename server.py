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

    if search is None or not search.strip():
          flash("You must provide a term to search")
          return render_template("mapform.html", doctors=[])

    doctors = db.session.execute("""
                            SELECT full_name, address, max(doctor_id) AS doctor_id, array_to_string(array_agg(specialty), ', ') AS specialty FROM 
                            (SELECT doctors.full_name, doctors.doctor_id, doctors.address, specialties.specialty
                            FROM doctors
                            INNER JOIN doctors_specialties ON doctors_specialties.doctor_id = doctors.doctor_id 
                            INNER JOIN specialties ON specialties.specialty_id = doctors_specialties.specialty_id) AS D
                            WHERE D.full_name ILIKE :search OR D.specialty ILIKE :search GROUP BY full_name, address;""",
                            {"search": f"%{search}%"}).fetchall()

    if not doctors:
        flash("We couldn't find anything related to your search")

    return render_template("mapform.html", doctors=doctors, search=search)

@app.route('/search.json')
def search_json():
    
    search = request.args.get("value_searched", None)  

    if search is None or not search.strip():
        return jsonify([])

    doctors = db.session.execute("""
                            SELECT full_name, address, longitude, latitude, max(doctor_id) AS doctor_id, array_to_string(array_agg(specialty), ', ') AS specialty FROM 
                            (SELECT doctors.full_name, doctors.doctor_id, doctors.address, specialties.specialty, doctors.longitude, doctors.latitude
                            FROM doctors
                            INNER JOIN doctors_specialties ON doctors_specialties.doctor_id = doctors.doctor_id 
                            INNER JOIN specialties ON specialties.specialty_id = doctors_specialties.specialty_id) AS D
                            WHERE D.full_name ILIKE :search OR D.specialty ILIKE :search GROUP BY full_name, address, longitude, latitude;""",
                            {"search": f"%{search}%"}).fetchall()


    return jsonify([{
        "full_name": doctor["full_name"],
        "address": doctor["address"],
        "coordinates": {"longitude": doctor["longitude"], "latitude": doctor["latitude"]}
    } for doctor in doctors])


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
        return redirect(url_for('login'))
 
    return render_template('registration.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route("/doctorform", methods=['GET', 'POST'])
# @login_required
def add_new_doctor_form():

    specialties = crud.get_specialties()

    #values as all none:

    # name = request.form.get("fullname")
    # specialty = request.form.get('doctor-specialty')
    # spanish = bool(request.form.get("spanish"))
    # portuguese = bool(request.form.get("portuguese"))
    # address = request.form.get("doctor-specialty")

    # values are not none, but specialty value is only from the first form:

    name = request.args.get("fullname")
    specialty = request.args.get('doctor-specialty')
    spanish = bool(request.args.get("spanish"))
    portuguese = bool(request.args.get("portuguese"))
    address = request.args.get("doctor-specialty")

    # what if the user adds two new "other" specialties
    # how this conditional would work?
    if specialty == "Other":
        specialty = request.args.get('other')


    # should my form be GET or POST then? 

    # import pdb
    # pdb.set_trace()   


    # new_doctor = crud.add_new_doctor(name, spanish, portuguese, address)
    # new_specialty = crud.add_a_new_specialty(specialty)

    return render_template('docform.html', specialties=specialties)


@app.route("/doctor/<doctor_id>", methods=["GET"])
# @login_required
def doctor(doctor_id):
    """Return profile of the given doctor."""

    doctor_id = doctor_id
    doctor_info = crud.get_doctor_by_id(doctor_id) 
    doctor_review = crud.get_review_by_doctor(doctor_id)

    for info in doctor_info:
        name = info.full_name 
        address = info.address
        portuguese = info.portuguese
        spanish = info.spanish
    
    if portuguese == False:
        portuguese = ""
    else:
        portuguese = "Portuguese" 

    if spanish == False:
        spanish = ""
    else:
        spanish = "Spanish" 

    return render_template("dprofile.html", 
                            doctor_id=doctor_id, 
                            doctor_name=name, 
                            address=address, 
                            portuguese=portuguese, 
                            spanish=spanish,
                            reviews=doctor_review)


@app.route("/review/<doctor_id>", methods=["GET", "POST"])
@login_required
def write_review(doctor_id):
    """Write and post a review for selected doctor"""

    doctor_id = doctor_id
    user_id = current_user.get_id()
    username = current_user.username  
    review = request.form.get("review")
    rating = request.form.get("rating")

    if review is None or not review.strip():
          flash("You must provide a valid text")
    else:
        review = crud.add_review(user_id, username, doctor_id, review, rating)
        flash("Thank you for submitting a review")
        return redirect(url_for('homepage'))
        # return redirect("/doctor/<doctor_id>") ?

    return render_template("review.html", id=doctor_id)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# import pdb
# pdb.set_trace()   

