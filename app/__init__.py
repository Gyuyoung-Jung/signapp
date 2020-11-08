# IMPORTS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# CONFIG
app = Flask(__name__, instance_relative_config=True)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# logging.basicConfig(filename='C:/dev/결재바람/signapp1/log/dummy.log', level=logging.INFO)
# logging.debug('this is a debug')
# logging.info('this is a info')
# logging.warning('this is a warning')

from app.views import app

