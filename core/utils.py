# -*- coding: utf-8 -*-
"""
Utilities for our views and models.
"""
import string
import random
import os
import re
import json
import logging
import traceback
import datetime as dtime
from datetime import datetime
from functools import wraps
from flask import request, send_from_directory, g, flash, redirect, url_for, session
from core import app
from uuid import uuid4


from threading import Thread
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def openPage(param):
  r = request.get(param)
  return r.json

def readfile(filepath):
    with open(filepath) as f:
        content = f.read()
    return content

def strip_input(data):
    return data.lower().strip()

def is_email_address_valid(email):
  """Validate email address using regular expression."""
  if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
      return False
  return True

def allowed_photos(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ['png', 'jpg', 'jpeg']

def format_avatar(photo):
  basename='user'
  suffix = datetime.now().strftime("%y%m%d_%H%M%S")
  imgname = "_".join([basename, suffix,'.jpg'])
  return imgname


def get_current_time(has_format=False):
  if has_format:
    return datetime.utcnow()
  return datetime.now()

def now():
    """Get timezone-aware UTC timestamp."""
    return dtime.datetime.now(dtime.timezone.utc)

def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))

def slugify(link):
    slug = re.sub(r"[^\w]+", " ", link)
    slug = "-".join(slug.lower().strip().split())
    return slug

def createSession(uid):
  session.pop('user_id', None)
  session['user_id'] = uid


"""
Untreated Markdown
"""
#from markdown import markdown as md4

"""
Manage multi-currency
"""
def get_currency():
  override = request.args.get('currency')
  if override:
    session['currency'] = override
  else:
    # use default currency
    session['currency'] = app.config.get('DEFAULT_CURRENCY')

  return session.get('currency', 'NGN')

class timeago(object):
    def __init__(self, interval):
        self.interval = interval

    def __repr__(self):
        return '<interval: %s>' % self.interval


"""

from flask.helpers import _endpoint_from_view_func


def add_quokka_url_rule(self, rule, endpoint=None,
                            view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        if not endpoint.startswith('quokka.'):
            endpoint = 'quokka.core.' + endpoint
        self.add_url_rule(rule, endpoint, view_func, **options)


app.add_quokka_url_rule('/tag/<tag>.xml',
                            view_func=TagRss.as_view('rss_tag'))

app.add_quokka_url_rule('/sitemap.xml',
                            view_func=SiteMap.as_view('sitemap'))


for filepath in app.config.get('MAP_STATIC_ROOT', []):
        app.add_quokka_url_rule(filepath, view_func=static_from_root)

"""