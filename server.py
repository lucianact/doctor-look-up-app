from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)
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
login_manager.login_view = "login"


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route("/")
def homepage():
    """Search health care providers by name or specialty."""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()
    
    search = request.args.get("value_searched")
    if search is None or not search.strip():
        flash("Please provide a term to search.")
        return render_template("homepage.html", doctors=[], all_doctors=all_doctors)
    
    # list of tuples with doctors info
    # (name, address, longitude, latitude, id, specialties)
    doctors_info = crud.provider_search(search)

    if not doctors_info:
        flash("We couldn't find anything related to your search.")

    if doctors_info:
        flash("Scroll down to check the search results.")

    # parse address to coordinates 
    # then add to the database:
    for info in doctors_info:
        address = info[1]
        longitude = info[2]
        latitude = info[3]
        id = info[4]
        if longitude is None or latitude is None:
            doctor = crud.get_doctor_by_id(id)
            for d in doctor:
                coordinates = geo_code(address)
                d.longitude = coordinates["longitude"]
                d.latitude = coordinates["latitude"]
                db.session.commit()

    return render_template("homepage.html", 
                            doctors=doctors_info,
                            search=search,
                            all_doctors=all_doctors)


@app.route("/search.json")
def search_json():
    """A JSON object generated by the user's search."""

    # this JSON object feeds the markers on the map
    # after the user has provided a search value

    search = request.args.get("value_searched", None)
    if search is None or not search.strip():
        return jsonify([])

    doctors_info = crud.provider_search(search)

    return jsonify(
        [
            {
                "id" : doctor["doctor_id"],
                "fullname": doctor["full_name"],
                "address": doctor["address"],
                "coordinates": {
                    "longitude": doctor["longitude"],
                    "latitude": doctor["latitude"],
                },
            }
            for doctor in doctors_info
        ]
    )


@app.route("/doctor-by-specialty/<doctor_specialty>")
def get_doctors_by_specialty(doctor_specialty):
    """A JSON object containing all database specialties."""

    # using for checking the specities in the databse

    doctors_by_specialty = []
    if doctor_specialty == "All":
        doctors_by_specialty = crud.get_doctors()
    else:
        doctors_by_specialty = crud.get_doctors_by_specialty(doctor_specialty)

    return jsonify(
        [
            {
                "full_name": doctor.full_name,
                "address": doctor.address,
                "coordinates": {
                    "longitude": doctor.longitude,
                    "latitude": doctor.latitude,
                },
            }
            for doctor in doctors_by_specialty
        ]
    )


@app.route("/signup", methods=["GET", "POST"])
def user_registration():
    """User registration form."""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    # registration using flask wtforms library
    # information from registration.py
    form = UserRegistration()
    username = form.username.data
    email = form.email.data
    password = form.password.data

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = crud.create_user(username, email, hashed_password)
        flash("Account succesfully created! Please log in to access your account.")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form, all_doctors=all_doctors)


@app.route("/login", methods=["GET", "POST"])
def login():
    """User lohgin form."""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    # login using flask-login library
    form = UserLogIn()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # hashing passwords with bycrypt library
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("homepage"))
        else:
            flash("Oh no! Something went wrong! Please check your password and username.")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form, all_doctors=all_doctors)


# The login manager contains the code that lets the application
# and Flask-Login work together such as
# how to load a user from an ID,
# where to send users when they need to log in,
# and so on:
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


@app.route("/logout")
def logout():
    """Log out the user."""
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/account")
@login_required
def user_account():
    """The user's account."""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()

    username = current_user.username
    user_id = current_user.get_id()

    # list of tuples
    # (content, date, username, doctor's ID, doctor's name)
    reviews_info = crud.reviews_info(user_id)

    # list o tuples
    # (favorite object, doctor's ID, doctor's name)
    doctors_liked = crud.doctors_liked_by_user(user_id)

    doctor_names = []
    for doctor in doctors_liked:
        doctor_names.append(doctor[2])

    return render_template(
        "account.html",
        username=username,
        reviews_info=reviews_info,
        doctors_liked=doctors_liked,
        all_doctors=all_doctors
    )


@app.route("/doctorform", methods=["GET", "POST"])
@login_required
def add_new_doctor_form():
    """Crowdsource feature."""

    all_doctors = crud.get_doctors()
    all_specialties = crud.get_specialties()

    if request.method == "POST":
        # data from docform:
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        fullname = first_name + " " + last_name + "*"
        # print(fullname)

        spanish = bool(request.form.get("spanish"))
        portuguese = bool(request.form.get("portuguese"))

        street_address = request.form.get("address")
        suite = request.form.get("suite")
        zip = request.form.get("zip")
        address = street_address + ", " + suite + ", San Francisco, CA " + zip
        # print(address)
        # print(request.form)

        form_specialties = request.form.getlist(
            "doctor-specialty"
        ) + request.form.getlist("other")
        # to get rid off empty strings:
        form_specialties = [
            specialty
            for specialty in form_specialties
            if specialty != "Other" and specialty != ""
        ]
        # to get unique values:
        form_specialties = set(form_specialties)
        form_specialties = list(form_specialties)
        # print(form_specialties)

        # add doctor to the database:
        if fullname not in all_doctors:
            new_doctor = crud.add_new_doctor(fullname, spanish, portuguese, address)

        # add (new) specialty to the database
        specialty_id_list = []
        for specialty in form_specialties:
            if specialty in all_specialties:
                specialty_id_list.append(specialty.specialty_id)
            else:
                new_specialty = crud.add_new_specialty(specialty)
                specialty_id_list.append(new_specialty.specialty_id)
        # print(specialty_id_list)

        # add new doctor and new specialties
        # to the doctors_specialties table:
        doctor_id = new_doctor.doctor_id
        new_link = crud.set_specialties(doctor_id, specialty_id_list)

    return render_template("docform.html", 
                            specialties=all_specialties,
                            all_doctors=all_doctors)


@app.route("/doctor/<doctor_id>", methods=["GET", "POST"])
# @login_required
def doctor(doctor_id):
    """The doctor's profile."""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()

    user_id = current_user.get_id()

    doctor_id = doctor_id  
    doctor_info = crud.get_doctor_by_id(doctor_id)
    doctor_reviews = crud.get_doctor_reviews(doctor_id)
    print(doctor_reviews)
 

    # unpacking doctor's info:
    for info in doctor_info:
        name = info.full_name
        address = info.address
        portuguese = info.portuguese
        spanish = info.spanish
   
    
    specialties = crud.get_specialty_by_doctor(name)
    specialties_string = ', '.join([str(specialty) for specialty in specialties]) 
    # print(specialties_string)

    # Portuguese/Spanish boolean values to strings:
    if portuguese == False:
        portuguese = ""
    else:
        portuguese = "Portuguese"

    if spanish == False:
        spanish = ""
    else:
        spanish = "Spanish"

    # allow the user to favorite this doctor
    is_favorited = crud.is_favorited(user_id, doctor_id)

    return render_template(
        "dprofile.html",
        doctor_id=doctor_id,
        doctor_name=name,
        address=address,
        portuguese=portuguese,
        spanish=spanish,
        specialties=specialties_string,
        reviews=doctor_reviews,
        is_favorited=is_favorited,
        all_doctors=all_doctors,
    )


@app.route("/review/<doctor_id>", methods=["GET", "POST"])
@login_required
def write_review(doctor_id):
    """Write and post a review for selected doctor"""

    # feeding base.html nav bar:
    all_doctors = crud.get_doctors()

    doctor_id = doctor_id
    doctor_name = crud.get_doctor_by_id(doctor_id)
    for name in doctor_name:
        dname = name.full_name

    user_id = current_user.get_id()
    username = current_user.username
    review = request.form.get("review")
    rating = request.form.get("rating")

    if review is None or not review.strip():
        flash("You must provide valid text.")
    else:
        review = crud.add_review(user_id, doctor_id, review, rating)
        flash("Thank you for submitting a review.")
        return redirect(url_for("user_account"))

    return render_template("review.html", 
                            id=doctor_id, 
                            doctor_name=dname, 
                            all_doctors=all_doctors
                            )


@app.route("/favorite/<int:doctor_id>", methods=["POST"])
@login_required
def add_favorites(doctor_id):
    """Bookmark doctor."""

    user_id = current_user.get_id()
    # print(user_id, doctor_id)
    favorite = crud.add_favorite(user_id, doctor_id)

    return jsonify({"isFavorited": True})


@app.route("/unfavorite/<int:doctor_id>", methods=["POST"])
@login_required
def delete_favorites(doctor_id):
    """Unbookmark doctor."""

    user_id = current_user.get_id()
    # print(user_id, doctor_id)
    unfavorite = crud.delete_favorite(user_id, doctor_id)

    return jsonify({"isFavorited": False})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



