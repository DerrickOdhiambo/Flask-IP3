import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config_options



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_name):
  app = Flask(__name__)

  # creating app configurations
  app.config.from_object(config_options[config_name])

  #initializing extensions
  login_manager.init_app(app)
  mail.init_app(app)
  db.init_app(app)
  bcrypt.init_app(app)


  #registering routes
  from app.main.views import main
  from app.users.views import users
  from app.posts.views import posts

  #registering the blueprints
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main)


  return app