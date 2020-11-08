from dataclasses import dataclass
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from datetime import datetime


@dataclass
class Document(db.Model):
    id: int
    title: str
    content: str
    status: str

    __tablename__ = 'document'
    __table_args__ = {'mysql_collate': 'utf8_unicode_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(4000), nullable=False)
    doc_type = db.Column(db.String(20), nullable=False)
    regdate = db.Column(db.DateTime, nullable=True)
    last_update_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(1), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User', foreign_keys=[sender_id], uselist=False, lazy='joined')
    receiver = db.relationship('User', foreign_keys=[receiver_id], uselist=False, lazy='joined')

    def __init__(self, title, content, doc_type, sender_id, receiver_id):
        self.title = title
        self.content = content
        self.doc_type = doc_type
        self.status = 'W'
        self.regdate = datetime.now()
        self.last_update_date = None
        self.sender_id = sender_id
        self.receiver_id = receiver_id

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
        return '<Document #{id} {doc_type} {s} -> {r}>'.format(id=self.id, doc_type=self.doc_type, s=self.sender.name, r=self.receiver.name)
        # return '<User {}>'.format(self.email)
