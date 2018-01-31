# -*- coding: utf-8 -*-

import logging
import datetime
from flask import (Blueprint, request, render_template, flash,
    g, session, redirect, url_for, json, Response)
from werkzeug import check_password_hash, generate_password_hash
from core.token import generate_confirmation_token, confirm_token

from core import app
from core import db

from core.users.forms import *
from flask_security import login_required, current_user

config = app.config

mod = Blueprint('home', __name__, url_prefix='')

@app.before_request
def before_request():
    from core.users.models import User
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@mod.route(r'/')
def index():
  # main page

  return render_template(
    'home.html', title = 'Find and Browse Music on %s ' %(config['BRAND']),\
    bdy_class = 'home', user=g.user,
    landing_pg=True
  )

@mod.route(r'/auth/login', methods=['GET', 'POST'])
def login():
  if g.user:
    return redirect(url_for('home.index'))

  next = ''
  if request.method == 'GET':
      if 'next' in request.args:
          next = request.args['next']

  form = LoginForm(request.form)

  return render_template('auth/signin.html', \
    title = 'Log In', form=form, next=next, bdy_class='auth')

@mod.route(r'/auth/forgot', methods=['GET', 'POST'])
def forgot():
  if g.user:
    return redirect(url_for('home.index'))

  next = ''
  if request.method == 'GET':
      if 'next' in request.args:
          next = request.args['next']

  form = LoginForm(request.form)

  return render_template('auth/forgot.html', \
    title = 'Forgot Password', form=form, next=next, bdy_class='auth')

@mod.route(r'/auth/signup', methods=['GET', 'POST'])
def register():
  if g.user:
    return redirect(url_for('home.index'))

  next = ''
  if request.method == 'GET':
      if 'next' in request.args:
          next = request.args['next']

  form = RegisterForm(request.form)

  return render_template('auth/signup.html', \
    form=form, title = 'Sign Up', next=next, bdy_class='auth')

@mod.route(r'/auth/logout', methods=['GET', 'POST'])
@login_required
def logout():
  session.pop('user_id', None)
  flash('Successfully logged out')
  return redirect(url_for('home.index'))



@mod.route(r'/account/verify/<token>', methods=['GET', 'POST'])
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The verification link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already verified. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmation_token = token
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account. Thanks!', 'success')
    return redirect(url_for('home.index'))