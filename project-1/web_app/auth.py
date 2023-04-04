
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Flask, abort
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
                abort(400)
        else:
            flash('Email is not registered', category='error')
            abort(400)

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


@auth.route('/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


# @app.errorhandler(400)
# def bad_request(e):
#     return jsonify(error=str(e)), 400

# @app.errorhandler(401)
# def unauthorized(e):
#     return jsonify(error=str(e)), 401


# @app.errorhandler(404)
# def not_found(e):
#     return jsonify(error=str(e)), 404


# @app.errorhandler(500)
# def internal_server_error(e):
#     return jsonify(error=str(e)), 500
