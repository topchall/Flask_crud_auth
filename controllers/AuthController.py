from flask import request, flash, url_for, render_template, redirect
from index import app, bcrypt, login_manager, db
# from config.db import cursor, connection
from models import User
from flask_login import login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
   return render_template('sign-in.html')

@app.route('/migrate')
def migrate():
   db.drop_all()
   db.create_all()
   return "done"

@app.route('/signup')
def signup():
   return render_template('sign-up.html')

@app.route('/register', methods = ['POST'])
def register():
   # cursor.execute(
   #      'SELECT ID FROM [dbo].[Users] ORDER BY ID DESC')
   # row = cursor.fetchone()
   # id = row[0] + 1
   firstName = request.form["firstName"]
   lastName = request.form["lastName"]
   email = request.form["email"]
   password = request.form["password"]
   repassword = request.form["confirmPassword"]
   if (firstName == '' or lastName == '' or email == '' or password == ''):
      flash('1')
      return redirect(url_for('signup'))
   if (password != repassword):
      flash('2')
      return redirect(url_for('signup'))
   user = User.query.filter_by(email=email).first()
   if user:
      flash('3')
      return redirect(url_for('signup'))
   hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
   # cursor.execute(
   #    "INSERT INTO dbo.Users (ID,FirstName,LastName,EMail,password) VALUES (?,?,?,?,?)", id, firstName, lastName, email, hashed_password
   # )
   # connection.commit()
   user = User(firstName = firstName, lastName = lastName, email = email, password = hashed_password) # Take user's data
   db.session.add(user) # Add the user to the database
   db.session.commit() # Commit changes to the database
   flash('0')
   return redirect(url_for('signup'))


@app.route('/login', methods = ['POST'])
def login():
   email = request.form["email"]
   password = request.form["password"]
   if (email == '' or password == ''):
      flash('1')
      return redirect(url_for('/'))
   user = User.query.filter_by(email=email).first()
   if user and bcrypt.check_password_hash(user.password, password):
      login_user(user)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('signup'))
   else:
      flash('2')
      return redirect(url_for('index'))