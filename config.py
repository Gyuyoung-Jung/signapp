import os
import logging
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'add-your-random-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://was:wjdrbdud1`@58.76.169.4:13306/sign'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 15
    MAIL_SERVER = 'smtp.mandrillapp.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-mandrill-username'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your mandrill-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your@default-mail.com'

    # LOGGING_LEVEL = logging.DEBUG
    # LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d'
    # LOGGING_LOCATION = 'C:/dev/결재바람/signapp1/log/'
    # LOGGING_FILENAME = 'test.log'
    # LOGGING_MAX_BYTES = 100000
    # LOGGING_BACKUP_COUNT = 100


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
