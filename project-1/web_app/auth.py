from flask import Blueprint, render_template, Flask, request, redirect, abort, url_for, jsonify, flash, session
from flask_login import login_required, current_user
from .models import User, Photo
from werkzeug.utils import secure_filename
import jwt
import os
from . import db
views = Blueprint('views', __name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = set(
    ['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'uploads'



@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    print('hi')
    if 'username_exists' in session:
        print('hi')
        username_exists = session['username_exists']
        user_exists = True

        return render_template('home.html', username=username_exists, user_exists=user_exists)
    print('hi')
    return render_template('home.html')


# View the public photos without authentication
# Ensure that this endpoint does not require authentication
@views.route('/get_public_photos', methods=['GET'])
def get_public_photos():
    photos_directory = '{}/public_photos'.format(os.getcwd())
    photos_list = os.listdir(photos_directory)
    return render_template('public_photos.html', photos=photos_list)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


def get_file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()

# File Handling


@views.route('/upload/<username>', methods=['POST', 'GET'])
def upload_files(username):
    if session['username_exists'] == username:
        file = request.files['file']
        filename = secure_filename(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_extension = get_file_extension(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Upload is successfully!!', category='success')
            file_info = Photo(filename=filename, filepath=os.path.join(
                app.config['UPLOAD_FOLDER']), user_id=username)
            db.session.add(file_info)
            db.session.commit()
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html', username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        filename = secure_filename(file.filename)
        filepath = '{}{}'.format(os.path.join(
            app.config['UPLOAD_FOLDER'])+'/', filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        print('{}'.format(file_size))
        if file_size == 0:
            flash('Upload a file in order to see the uploads', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html', username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        elif file_size > app.config['MAX_CONTENT_LENGTH']:
            flash('Max file size reached', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html', username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        else:
            flash('Enter correct format', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html', username=username_exists, user_exists=user_exists)
            return render_template('home.html')
