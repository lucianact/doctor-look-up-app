#  There are two possible ways to handle a user registration scenario

#  WAY 1

# Display a HTML form:
#
# {% extends 'base.html' %}
# {% block title %}User registration{% endblock %}
#
# <h2>Create an Account</h2>
# <form action="/users" method="POST">
#   Email <input type="text" name="email">
#   Password <input type="password" name="password">
#   <input type="submit">
# </form>
#
# {% endblock %}

# In server.py created a route to process the form
# and to add the new user to the data base:
#
# @app.route('/users', methods=['POST'])
# def register_user():
#     """Create a new user."""
#
#     email = request.form.get('email')
#     password = request.form.get('password')
#
#     user = crud.get_user_by_email(email)
#     if user:
#         flash('User already exists')
#     else:
#         crud.create_user(email, password)
#         flash('Account created! Please log in.')
#
#     return redirect('/')
#
#  To add the user to the database, we have to define
#   the functions "get_user_by_email(email)" & "creat_user" in crud.py:
#
# def get_user_by_email(email):
#   """Return a user by email."""
#
#   return User.query.filter(User.email == email).first()
#
# def create_user(email, password):
#   """Create and return a new user."""
#
#   user = User(email=email, password=password)
#   db.session.add(user)
#   db.session.commit()
#
#   return user

# And finally, to be able to add a new user to the database,
# we need a user table in model.py:
#
# class User(db.Model):
#   """A user."""
#
#   __tablename__ = 'users'
#
#   user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#   email = db.Column(db.String, unique=True)
#   password = db.Column(db.String)
#   ratings = a list of Rating objects
#
#   def __repr__(self):
#   return f'<User user_id={self.user_id} email={self.email}>'

# Questions:
# What about the .sql file?
# What about PostgreSQL?

# To add sessions:
#
#  1. In server.py
#  from flask import session
#
#  (session is going to be dictionary-like type of object)
#
#   when the user registers or logs in,
#   save his "name" or e-mail in this session dictionary-like object:
#
#   In the HTML file:
# <form action='/login'>
#
# <label for="uname"><b>Username</b></label>
# <input type="text" placeholder="Enter Username" name="uname" required>
#
# <label for="psw"><b>Password</b></label>
# <input type="password" placeholder="Enter Password" name="psw" required>
#
# <button type="submit">Login</button>
# </form>
# <label>
# <input type="checkbox" checked="checked" name="remember"> Remember me
# </label>
#
# In server.py
# @app.route('/log-in')
# def get_name():
#   """Get name from homepage form and store name in session."""
#
#   username = request.args.get('username')
#   session['name'] = username
#   return redirect('/')
