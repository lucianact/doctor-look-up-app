"""Server for latin doctor search web app."""

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from model import connect_to_db, User, db, Review, Doctor
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

    doctors = crud.health_provider_search(search)

    if not doctors:
        flash("We couldn't find anything related to your search")

    return render_template("mapform.html", doctors=doctors, search=search)

@app.route('/search.json')
def search_json():
    
    search = request.args.get("value_searched", None)  

    if search is None or not search.strip():
        return jsonify([])

    doctors = crud.map_search(search)

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
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash("You're logged in!")
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
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

    username = current_user.username
    user_id = current_user.get_id()
   
    info = crud.reviews_info(user_id)
    print(info)

    doctors_liked = crud.doctors_liked_by_user(user_id)
    print(doctors_liked)

    doctors_liked_id = []
    doctors_liked_name = []

    for element in doctors_liked:
        doctors_liked_id.append(element[1])
        doctors_liked_name.append(element[2])
    
    print(doctors_liked_id)
    print(doctors_liked_name)

    doctors = []
    ids = []
    reviews = []

    for element in info:
        doctors.append(element[4])
        ids.append(element[3])
        reviews.append(element[0])

    print(ids)
    print(doctors)
    print(reviews)

    return render_template('account.html', 
                            username=username, 
                            doctors=doctors, 
                            reviews=reviews, 
                            ids=ids,
                            doctors_liked_id=doctors_liked_id,
                            doctors_liked_name=doctors_liked_name)


@app.route("/doctorform", methods=['GET','POST'])
# @login_required
def add_new_doctor_form():

    doctors = crud.get_doctors()
    print(doctors)

    specialties = crud.get_specialties()
    print(specialties)

    if request.method == 'POST':

        # info for doctors table:
        name = request.form.get("fullname")
        spanish = bool(request.form.get("spanish"))
        portuguese = bool(request.form.get("portuguese"))
        address = request.form.get("address")

        # print(request.form)

        # info for specialty table: 
        form_specialties = request.form.getlist("doctor-specialty") + request.form.getlist("other")
        print(form_specialties)
        form_specialties = [specialty for specialty in form_specialties if specialty != "Other" and specialty!= ""] # list comprehension
        print(form_specialties)
        
        # for unique values
        form_specialties = set(form_specialties)
        form_specialties = list(form_specialties)

        if name not in doctors:
            new_doctor = crud.add_new_doctor(name, spanish, portuguese, address)
        
        specialty_id_list = []
        for specialty in form_specialties:
            if specialty in specialties:
                specialty_id_list.append(specialty.specialty_id)
            else: 
                new_specialty = crud.add_new_specialty(specialty)
                specialty_id_list.append(new_specialty.specialty_id)
        
        print(specialty_id_list)

        doctor_id = new_doctor.doctor_id
        
        new_link = crud.set_specialties(doctor_id, specialty_id_list)


    return render_template('docform.html', specialties=specialties)


@app.route("/doctor/<doctor_id>", methods=["GET", "POST"])
# @login_required
def doctor(doctor_id):
    """Return profile of the given doctor."""

    doctor_id = doctor_id
    doctor_info = crud.get_doctor_by_id(doctor_id) 
    doctor_review = crud.get_doctor_reviews(doctor_id)
    print(doctor_review)
    user_id = current_user.get_id()
    is_favorited = crud.is_favorited(user_id, doctor_id)

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
                            reviews=doctor_review,
                            is_favorited=is_favorited)


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
        review = crud.add_review(user_id, doctor_id, review, rating)
        flash("Thank you for submitting a review")
        return redirect(url_for('homepage'))
        # return redirect("/doctor/<doctor_id>") ?

    return render_template("review.html", id=doctor_id)


@app.route("/favorite/<int:doctor_id>", methods=["POST"])
@login_required
def add_favorites(doctor_id):

    user_id = current_user.get_id()
    print(user_id, doctor_id)

    favorite = crud.add_favorite(user_id, doctor_id)

    return jsonify({"isFavorited" : True})

@app.route("/unfavorite/<int:doctor_id>", methods=["POST"])
@login_required
def delete_favorites(doctor_id):

    user_id = current_user.get_id()
    print(user_id, doctor_id)
    unfavorite = crud.delete_favorite(user_id, doctor_id)


    return jsonify({"isFavorited" : False})



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# import pdb
# pdb.set_trace()   

