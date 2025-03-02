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
    MONGO_HOST = os.getenv("MONGO_HOST", "nsql-mongodb-1")
    app.config['MONGO_USER'] = os.getenv('MONGO_USER')
    app.config['MONGO_PASSWORD'] = os.getenv('MONGO_PASSWORD')    
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.debug = True 
    
    


    
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    logging.basicConfig(level=logging.DEBUG)

    from app.routes import main
    app.register_blueprint(main)

    return app
