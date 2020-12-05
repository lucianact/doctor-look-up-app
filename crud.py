from model import (
    db,
    Doctor,
    Specialty,
    DoctorSpecialty,
    User,
    Review,
    Favorite,
    connect_to_db,
)
from flask_sqlalchemy import SQLAlchemy
from geocode import geo_code


def get_all_doctors_and_specialties():
    """Return all doctors and all specialties from database."""

    result = []

    output = db.session.query(Doctor).join(DoctorSpecialty).join(Specialty).all()

    for doctor in output:
        specialty_list = []
        for special_link in doctor.doctors_specialties:
            specialty_list.append(special_link)

        result.append(specialty_list)

    return result


def get_doctors_by_specialty(user_input):
    """Return all doctors by specific specialty."""

    return (
        Doctor.query.join(DoctorSpecialty)
        .join(Specialty)
        .filter(Specialty.specialty == user_input)
        .all()
    )


def get_specialty_by_doctor(user_input):
    """Return all specialties from specific doctor."""

    return (
        Specialty.query.join(DoctorSpecialty)
        .join(Doctor)
        .filter(Doctor.full_name == user_input)
        .all()
    )


def get_specialties():
    """Return all specialties."""
    return Specialty.query.all()


def get_doctors():
    """Return all doctors."""
    return Doctor.query.all()


def get_doctor_by_id(doctor_id):
    """Return doctors by their ID."""
    return Doctor.query.filter(Doctor.doctor_id == doctor_id).all()


def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, 
                email=email, 
                password=password
                )

    db.session.add(user)
    db.session.commit()

    return user


def check_username(username):
    """Check if username already exists in the database."""
    return User.query.filter(User.username == username).first()


def check_email(email):
    """Check if e-mail already exists in the database."""
    return User.query.filter(User.email == email).first()


def add_new_doctor(full_name, spanish, portuguese, address):
    """Add a new doctor to the database."""

    new_doctor = Doctor(
        full_name=full_name, spanish=spanish, portuguese=portuguese, address=address
    )

    db.session.add(new_doctor)
    db.session.commit()

    return new_doctor


def add_new_specialty(specialty):
    """Add a new specialty to the database."""

    new_specialty = Specialty(specialty=specialty)
    db.session.add(new_specialty)
    db.session.commit()

    return new_specialty


def set_specialties(doctor_id, specialty_ids):
    """Connect doctors with to specialties."""

    new_links = []

    for id in specialty_ids:
        new_link = DoctorSpecialty(doctor_id=doctor_id, specialty_id=id)
        new_links.append(new_link)
        db.session.add(new_link)

    db.session.commit()

    return new_links


def add_review(user_id, doctor_id, review_content):
    """Add review to the database."""

    review = Review(
        user_id=user_id,
        doctor_id=doctor_id,
        review_content=review_content
    )

    db.session.add(review)
    db.session.commit()

    return review


def get_doctor_reviews(doctor_id):
    """Get review by doctor ID."""
    return Review.query.filter(Review.doctor_id == doctor_id).all()


def get_reviews_by_user(user_id):
    """Get revie user ID."""
    return Review.query.filter(Review.user_id == user_id).all()


def reviews_info(user_id):
    """Return reviews info."""

    info = (
        db.session.query(
            Review,
            User.username,
            Doctor.doctor_id,
            Doctor.full_name,
        )
        .join(Doctor)
        .join(User, User.user_id == Review.user_id)
        .filter(Review.user_id == user_id)
        .all()
    )

    return info


def add_favorite(user_id, doctor_id):
    """Add doctor to favorites table."""

    favorite = Favorite(user_id=user_id, doctor_id=doctor_id)
    db.session.add(favorite)
    db.session.commit()


def delete_favorite(user_id, doctor_id):
    """Delete doctor from favorites table."""

    favorites = Favorite.query.filter(
        Favorite.user_id == user_id, Favorite.doctor_id == doctor_id
    ).all()

    for fav in favorites:
        db.session.delete(fav)

    db.session.commit()


def is_favorited(user_id, doctor_id):
    """Check favorited doctors."""

    favorited = Favorite.query.filter(
        Favorite.user_id == user_id, Favorite.doctor_id == doctor_id
    ).count()
  
    return favorited


def doctors_liked_by_user(user_id):
    """Return doctors liked by user ID."""
    
    doctors = (
        db.session.query(Favorite, Doctor.doctor_id, Doctor.full_name)
        .join(Doctor)
        .join(User, User.user_id == Favorite.user_id)
        .filter(Favorite.user_id == user_id)
        .all()
    )

    return doctors


def provider_search(search):
    """Search for doctors and specialties from the database."""

    doctors = db.session.execute(
        """
                            SELECT full_name, address, longitude, latitude, max(doctor_id) AS doctor_id, array_to_string(array_agg(specialty), ', ') AS specialty FROM 
                            (SELECT doctors.full_name, doctors.doctor_id, doctors.address, specialties.specialty, doctors.longitude, doctors.latitude
                            FROM doctors
                            INNER JOIN doctors_specialties ON doctors_specialties.doctor_id = doctors.doctor_id 
                            INNER JOIN specialties ON specialties.specialty_id = doctors_specialties.specialty_id) AS D
                            WHERE D.full_name ILIKE :search OR D.specialty ILIKE :search GROUP BY full_name, address, longitude, latitude;""",
        {"search": f"%{search}%"},
    ).fetchall()

    return doctors
    

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
