import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.debug = True 

    
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    logging.basicConfig(level=logging.DEBUG)

    from app.routes import main
    app.register_blueprint(main)

    return app
