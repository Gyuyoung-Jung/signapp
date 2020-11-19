from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_unicode_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nid = db.Column(db.Integer, unique=True, nullable=True)
    kid = db.Column(db.Integer, unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    nickname = db.Column(db.String(100), nullable=True)
    push_token = db.Column(db.String(100), unique=True, nullable=True)
    get_push = db.Column(db.String(1), nullable=False)
    device = db.Column(db.String(1), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    regdate = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    access_token = db.Column(db.String(100), nullable=True)
    refresh_token = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(10), default='user')

    def __init__(self, nid, kid, email, name, nickname, push_token, get_push, device, role='user'):
        self.nid = nid
        self.kid = kid
        self.email = email
        self.name = name
        self.nickname = nickname
        self.push_token = push_token
        self.get_push = get_push
        self.device = device
        self.authenticated = False
        self.regdate = datetime.now()
        self.last_logged_in = datetime.now()
        self.current_logged_in = datetime.now()
        self.role = role

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all user are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous user aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def get_email(self):
        return str(self.email)

    def __repr__(self):
        return '<User {}>'.format(self.email)
