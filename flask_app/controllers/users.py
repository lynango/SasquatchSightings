from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#Shows the front page
@app.route('/')
def index():
    return render_template('front_page.html')

#Process user's request to register
@app.route('/register',methods=['POST'])
def register():
    if not User.registration(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

#Process user's request to login
@app.route('/login',methods=['POST'])
def login():
    data = {"email": request.form['email']} 
    user_with_email = User.get_by_email(data) 
    if user_with_email == False:
        flash("Invalid Email/Password") 
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']): 
        flash("Invalid Email/Password") 
        return redirect('/')
    session['user_id'] = user_with_email.id
    return redirect('/dashboard') 


#Validation checkpoint for logged in users
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')  # ->Checks to see if the user had login or not. If not, the user is redirected to the front page.
    data ={
        'id': session['user_id']    # ->If the user had login, the user is directed to the dashboard.
    }
    one_user = User.get_one(data)
    sightings = Sighting.get_all_with_reporter()                                                                                                                                               
    return render_template("dashboard.html", current_user = one_user, all_sightings = sightings)

#Process user's request to logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')