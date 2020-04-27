from zakupy_dla_seniora import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column('content', db.String(500), nullable=False)
    contact_number = db.Column('contact_number', db.String(12), nullable=False)
    location = db.Column('location', db.String(100))
    longitude = db.Column('longitude', db.Float(precision=5))
    latitude = db.Column('latitude', db.Float(precision=5))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column('created_by', db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column('created_at', db.DateTime)
    status = db.Column('status', db.String(60))
    error = db.Column('error', db.String(500))

    def __init__(self, content, contact_number, status, location=None, latitude=None, longitude=None, created_by=None):
        self.content = content
        self.contact_number = contact_number
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.created_at = datetime.now(timezone.utc)
        self.created_by = created_by

    def __repr__(self):
        return "Message : ".format(self.content, self.contact_number, self.location, self.status)

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_received(cls):
        return cls.query.filter_by(status='received').all()

    @classmethod
    def get_user_messages(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_phone(cls, phone_):
        return cls.query.filter_by(contact_number=phone_).order_by(Message.created_at.desc()).first()

    @classmethod
    def get_errors(cls):
        return cls.query.filter_by(status='error').order_by(Message.created_at.desc()).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
