__author__ = 'mrlaolu'
__description__ = 'managing other tables'

import datetime   

from core import db, app
from core.utils import slugify

config = app.config

class ContactUs(db.Model):

    __tablename__='contactus'

    id=db.Column(db.Integer, primary_key=True)
    sender=db.Column(db.String(120))
    email=db.Column(db.String(245))
    phone=db.Column(db.String(120))
    note=db.Column(db.String(255))
    sent_at = db.Column(db.DateTime, default=db.func.now())
    sender_ip = db.Column(db.String(15))
    last_browser = db.Column(db.String(254))
    read = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, sender, email, note, sender_ip):
        self.sender=sender
        self.email=email
        #self.phone=phone
        self.note=note
        self.sender_ip=sender_ip

    def __repr__(self):
        return '<Contact Us %r>' % (self.sender)

class Country(db.Model):
    """
    A location where humans are listed, using geoid for primary key.
    """    
    __tablename__='countries'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    code=db.Column(db.String(5))
    phone=db.Column(db.String(10))
    slug=db.Column(db.String(120))
    icon=db.Column(db.String(120)) 
    users=db.relationship('Profile', backref='countries', lazy='dynamic') 

    def __init__(self, id, code, name, phone):
        self.id=id
        self.code=code
        self.name=name
        self.phone=phone
        self.slug=slugify(self.name)

    def __repr__(self):
        return '<Country %r>' % (self.name)

    def count_cities(self):
        rs=self.city
        return rs.count()