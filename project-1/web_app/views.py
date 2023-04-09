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


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in {'jpg', 'png'}

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    print('hi')
    if 'username_exists' in session:
                print('hi')
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html',username=username_exists, user_exists=user_exists)
    print('hi')
    return render_template('home.html')
@views.route('/get_public_photos', methods=['GET'])
def get_public_photos():
    photos_directory = 'C:\Programming\CPSC_449\project-1\public_photos'
    photos_list = os.listdir(photos_directory)
    return render_template('public_photos.html', photos=photos_list)

# @views.route('/upload_public_photos', methods=['POST'])
# @login_required
# def upload_public():
#     token = request.headers.get('Authorization', None)

#     if token:
#         try:
#             decoded_token = jwt.jwt_decode_callback(token)
#             username = decoded_token['user_id']
#             user = User.query.filter_by(email=username).first()
#             if user:
#                 if 'file' not in request.files:
#                     return 'No file provided', 400

#                 file = request.files['file']
#                 # user_id = request.form.get('user_id')  # Get user ID from form data

#                 # Check file type and size
#                 if file and allowed_file(file.filename) and file.content_length <= 16 * 1024 * 1024:
#                     # Generate a secure filename and save the file to a directory
#                     filename = secure_filename(file.filename)
#                     file.save(os.path.join('uploads', filename))
#                     # Save file path and user ID in the database
#                     filepath = os.path.join('uploads', filename)
#                     new_file = Photo(filename=filename, filepath=filepath, user_id=user.id)
#                     db.session.add(new_file)
#                     db.session.commit()

#                     return 'File uploaded successfully', 201
#                 else:
#                     return 'Invalid file type or file size exceeded (16MB)', 400
#         except:
#             pass
#     else:
#         return redirect('/login')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


def get_file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()


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
            file_info = Photo(filename=filename, filepath=os.path.join(app.config['UPLOAD_FOLDER']), user_id=username)
            db.session.add(file_info)
            db.session.commit()
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html',username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        filename = secure_filename(file.filename)
        filepath = '{}{}'.format(os.path.join(app.config['UPLOAD_FOLDER'])+'/',filename)
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        print('{}'.format(file_size))
        if file_size == 0:
            flash('Upload a file in order to see the uploads', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html',username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        elif file_size > app.config['MAX_CONTENT_LENGTH']:
            flash('Max file size reached', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html',username=username_exists, user_exists=user_exists)
            return render_template('home.html')
        else:
            flash('Enter correct format', category='error')
            os.remove(filepath)
            if session['username_exists']:
                username_exists = session['username_exists']
                user_exists = True

                return render_template('home.html',username=username_exists, user_exists=user_exists)
            return render_template('home.html')