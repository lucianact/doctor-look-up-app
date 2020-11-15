from model import db, Doctor, Specialty, DoctorSpecialty, User, connect_to_db
from flask_sqlalchemy import SQLAlchemy
from geocode import geo_code


def get_all_doctors_and_specialties():
    """Return all doctors and all specialties from database"""

    result = []

    output = db.session.query(Doctor).join(DoctorSpecialty).join(Specialty).all()

    for doctor in output:
        specialty_list = []
        for special_link in doctor.doctors_specialties:
            specialty_list.append(special_link)
    
        # import pdb
        # pdb.set_trace()

        result.append(specialty_list)
    
    return result

def get_doctors_by_specialty(user_input):
    """Return all the doctors of a specific specialty"""

    return Doctor.query.join(DoctorSpecialty).join(Specialty).filter(Specialty.specialty == user_input).all()

def get_specialty_by_doctor(user_input):
    """Return all the specialties of  a specific doctor"""

    return Specialty.query.join(DoctorSpecialty).join(Doctor).filter(Doctor.full_name == user_input).all()

def get_specialties():
    """Return all specialties."""

    return Specialty.query.all()

def get_doctors():
    """Return all doctors."""

    return Doctor.query.all()

def get_doctor_by_id(doctor_id):
    """Return doctor by its ID."""

    return Doctor.query.filter(Doctor.doctor_id==doctor_id).all()

def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit() 

    return user

def check_username(username):
    """Check if an user username already exists in the database."""

    return User.query.filter(User.username==username).first()

def check_email(email):
    """Check if an user e-mail already exists in the database."""

    return User.query.filter(User.email==email).first()

def add_new_doctor(full_name, spanish, portuguese, address):
    """Add a new doctor to the database."""

    new_doctor = Doctor(full_name=full_name, spanish=spanish, portuguese=portuguese, address=address)

    db.session.add(new_doctor)
    db.session.commit() 

    return new_doctor

def add_a_new_specialty(specialty):
    """Add a new doctor to the database."""

    new_specialty = Specialty(specialty=specialty)

    db.session.add(specialty)
    db.session.commit() 

    return new_specialty

# def check_user_by_username(username):
#     """Check if user already exists in the database"""

#     return User.query.filter_by(username).first()
         
    
# def check_user_username(username):
#     """Check if an user username already exists in the database."""

#     return User.query.filter_by(username).first()

# def check_user_email(email):
#     """Check if an user e-mail already exists in the database."""

#     return User.query.filter_by(email).first()

# def tests():

    # Doctors who speak portuguese:
    # return Doctor.query.filter(Doctor.portuguese == True).all()

    # Doctors who speak spanish:
    # return Doctor.query.filter(Doctor.spanish == True).all()

    # Doctors who speak portuguese and spanish:
    #return Doctor.query.filter((Doctor.portuguese == True) & (Doctor.spanish == True)).all()

    # Doctors who speak portuguese or spanish: 
    # return Doctor.query.filter((Doctor.portuguese == True) | (Doctor.spanish == True)).all()
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)



    # print(get_doctors())
    # print(get_all_doctors_and_specialties())
    # print(get_doctors_by_specialty('Chiropractor'))
    print(get_doctor_by_id(1))