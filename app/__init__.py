from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)

#sqlalchemy database instances
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#flask-login instance
login = LoginManager(app)
login.login_view = 'login'

#loging and email configuration
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s:%(message)s - [in %(pathname)s:%(line)d]'))
    file_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.setLevel(logging.ERROR)
    app.logger.info('Micrblog startup')


from app import routes, models, errors