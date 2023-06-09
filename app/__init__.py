from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.lib.auth_token import AuthToken
from config import config
from flask_pagedown import PageDown

from .lib.auth_token import AuthToken

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  bootstrap.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  pagedown.init_app(app)
  AuthToken.setup(app.config['MSG_KEY'])

  if app.config['SSL_REDIRECT']:
    from flask_sslify import SSLify
    sslify = SSLify(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  from .controller import api as api_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api/v1')

  return app
