from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime


class Approval(db.Model):
    __tablename__ = 'approval'
    __table_args__ = {'mysql_collate': 'utf8_unicode_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(4000), nullable=False)
    regdate = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.String(1), nullable=False)
    sender = db.relationship('User', backref='user', lazy='dynamic')
    receiver = db.relationship('User', backref='user', lazy='dynamic')

    def __init__(self, nid, email, name, role='user'):
        self.nid = nid
        self.email = email
        self.name = name
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role

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
