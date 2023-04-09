from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jeetpatel'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User
    from .models import Photo

    with app.app_context():
        db.create_all()

    manage_login = LoginManager()
    manage_login.login_view = 'auth.login'
    manage_login.init_app(app)

    @manage_login.user_loader
    def user_load(id):
        return User.query.get(int(id))    


    return app

def database_create(app):
    if not path.exists('web_app/' + DB_NAME):
        db.create_all(app=app)
        print("Database created successfully")