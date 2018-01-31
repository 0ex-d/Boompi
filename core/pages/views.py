# -*- coding: utf-8 -*-

import logging
import datetime
from flask import (Blueprint, request, render_template, flash,
    g, session, redirect, url_for, json, Response)
from werkzeug import check_password_hash, generate_password_hash

from core import app
from core import db

from core.pages.forms import ContactForm
from flask.ext.login import login_user, logout_user, \
      login_required, current_user


mod = Blueprint('pages', __name__, url_prefix='')

#globals
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format='%(message)s', level=logging.INFO)


@app.before_request
def before_request():
    from core.users.models import User
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

"""
Content
"""

@mod.route('/about')
def about():
    return render_template('company/about.html', title='About', bdy_class='content', user=g.user)

@mod.route('/how-it-works')
def how_it_works():
    form = ContactForm(request.form)
    return render_template('company/how-it-works.html', title='About', bdy_class='content', form=form, user=g.user)

@mod.route('/contact-us')
def contact_us():
    form = ContactForm(request.form)
    return render_template('company/contact.html', title='About', bdy_class='content', form=form, user=g.user)

@mod.route('/terms-of-service')
def terms():
    return render_template('company/terms.html', title='Terms of Service', bdy_class='content', user=g.user)

@mod.route('/privacy-policy')
def privacy():
    return render_template('company/privacy.html', title='Privacy Policy', bdy_class='content', user=g.user)