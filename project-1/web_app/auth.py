
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Flask, abort, session
from . import db
import jwt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from .models import User, Photo
import datetime
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
auth = Blueprint('auth', __name__)

public_items = ['public_item1', 'public_item2', 'public_item3']

def e(message, status_code):
    response = {
        'error': {
            'message': message,
            'status': status_code
        }
    }
    return response, status_code

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        username_exists = user.username
        # username_exists = User.query.filter_by(username=user.username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!!', category='success')
                login_user(user, remember=True)

                token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm='HS256')

                session['username_exists'] = user.username
                session['token'] = token
                session.permanent = True


                user_exists = True

                # data = jsonify({'token':token})
                # return jsonify({'token':token})
                return render_template('home.html',username=username_exists, user_exists=user_exists)
            else:
                flash('Incorrect password', category='error')
                return jsonify({'message':'Incorrect Password'}),401        
        else:
            flash('Email is not registered', category='error')
            return jsonify({'message':'Incorrect Email'}),401  



    return render_template('login.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('User exists', category='error')
        elif username_exists:
            flash('Username in use', category='error')
        elif len(email) < 4:
            flash('Invalid email', category='error')
        elif len(username) < 2:
            flash('Username is short', category='error')
        elif len(password) < 6:
            flash('Password is short', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User profile created!!')
            return redirect(url_for('views.home'))

    email_exists = User.query
    return render_template('signup.html')

@auth.route('/private-pics', methods=['GET', 'POST'])
def private_pics():
    
    try:
        if 'username_exists' not in session:
            flash('Unauthorized',category='error')
            return render_template('home.html'),401
        decoded = jwt.decode(session['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
        print(decoded['user_id'])

        user = User.query.get(decoded['user_id'])
        name = user.username
        print(name)
        photos = Photo.query.filter_by(user_id=name).all()
        filenames = [file.filename for file in photos]
        return render_template('private-pics.html', photos=filenames)
    except jwt.ExpiredSignatureError:
        flash("Token has expired.", category='error')
    except jwt.InvalidTokenError:
        flash('Token is invalid', category='error')
    return render_template('home.html')



# @app.route('/upload/<username>', methods=['POST','GET'])
# def upload_file(username):
#     # Check if user is logged in
#     if 'username' not in session:
#         return redirect('/login')
#     if session['username_exists'] != username:
#         return jsonify({'message': 'Invalid username'}), 401
    
@auth.route('/logout')
@login_required
def logout():
    if session['username_exists']:
        session.pop('username_exists')
        # session.pop('token')
        return render_template('home.html')
    return render_template('home.html')


@app.errorhandler(400)
def bad_request(e):
    message = "The server could not understand the request due to invalid syntax."
    return e(message, 400)

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    return jsonify({
        "status": 500,
        "message": "Internal server error",
    }), 500

@app.errorhandler(400)
def handle_bad_request(e):
    """Handle 400 Bad Request errors"""
    return jsonify({
        "status": 400,
        "message": "Bad Request",
    }), 400

@app.errorhandler(401)
def handle_unauthorized(e):
    """Handle 401 Unauthorized errors"""
    return jsonify({
        "status": 401,
        "message": "Unauthorized",
    }), 401

@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 Not Found errors"""
    return jsonify({
        "status": 404,
        "message": "Not Found",
    }), 404