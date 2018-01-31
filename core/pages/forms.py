# -*- coding: utf-8 -*-

"""
"""
import re
from flask.ext.wtf import Form
from wtforms import (
    StringField, TextAreaField, 
    PasswordField, BooleanField, 
    FileField, SelectField, RadioField
)
from wtforms.validators import Required, EqualTo, Email, URL, Length

class ContactForm(Form):
    sender = StringField('Full Name', [Required()])
    email = StringField('Email address', [Required(), Email()])
    school = StringField('School', [Required()])
    phone = StringField('Phone Number', [Required()])
    note = TextAreaField('Note', [Required()])