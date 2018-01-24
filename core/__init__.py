#!/usr/bin/python3
# -*- coding: utf-8 -*-
VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Ready"
__description__ = "Boompi"
__author__ = "Laolu Akindolire <mrlaolu@gmx.com>"
__license__ = "Proprietary Software"
__copyright__ = "Copyright 2017, Kindo Labs"


###########
# imports #
###########
import os
import os.path as op
from datetime import datetime
from flask import Flask, render_template, abort, \
request, url_for, redirect, send_from_directory, json, Response
from werkzeug.routing import BaseConverter

from flask_security import Security, SQLAlchemyUserDatastore, \
UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password

from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

from sqlalchemy import func

from core.momentjs import momentjs

import flask_admin as myadmin
from flask_admin import Admin 
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import helpers as admin_helpers

##########
# config #
##########

app = Flask(__name__)
#env = os.environ.get('APP_ENV')

config = app.config

#config.from_object('config.%sConfig' % env.capitalize())

# for MS windows only 
env = 'development'
config.from_object('config.%sConfig' % env.capitalize())

app.jinja_env.globals['momentjs'] = momentjs


##############
# extensions # 
##############

db = SQLAlchemy(app)
csrf= CsrfProtect(app)
mail = Mail(app)

@app.template_filter()
def copyyear():
    value=datetime.now()
    return value.strftime('%y')

@app.template_filter()
def blogdatetime(value, format='%d %b, %Y at %I:%M %p'):
    """convert a datetime to a different format."""
    return value.strftime(format)
    
@app.template_filter('formatdate')
def format_datetime_filter(input_value, format_="%a, %d %b %Y"):
    return input_value.strftime(format_)

@app.template_filter()
def currency(amount):
    currency = config['CURRENCY']
    currency_code = currency['NGN']['symbol']
    return '{}{:,.0f}'.format(currency_code, amount)






from core.models import *
from core.users.models import *
from core.tracks.models import *


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


##############
# blueprints #
##############

from core.users.views import mod as base_module
app.register_blueprint(base_module)

from core.home.views import mod as base_module
app.register_blueprint(base_module)

from core.tracks.views import mod as base_module
app.register_blueprint(base_module)

from core.pages.views import mod as base_module
app.register_blueprint(base_module)


from core.ajax import mod as base_module
app.register_blueprint(base_module)


# Setup Flask-Admin
admin = Admin(
    app,
    name='Dashboard',
    url='/dashboard/1111',
    base_template='admin/my_master.html', template_mode='bootstrap3'
)

from wtforms.fields import PasswordField

# Custom model view class
class BaseMV(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return current_user.has_role('admin') or current_user.has_role('moderator')

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('home.login', next=request.url))


class UserMV(BaseMV):
    # Don't display the password on the list of Users
    #column_exclude_list = ('password','salt','reset_password_token','confirmation_token','confirmed_on', 'username')

    #column_searchable_list = ('fullname')

    # Don't include the standard password field when creating or editing a User (but see below)
    #form_excluded_columns = column_exclude_list

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserMV, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = generate_password_hash(model.password2)

# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')



'''
class JobMV(BaseMV):
    column_searchable_list = ('title',)

class JobMainMV(BaseMV):
    column_exclude_list = ('cv_required',)



#admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
# Add administrative views here
admin.add_view(UserMV(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))


admin.add_view(JobMainMV(Job, db.session))
admin.add_view(JobMV(JobCategory, db.session))
admin.add_view(JobMV(JobSubCategory, db.session))
admin.add_view(BaseMV(JobRequest, db.session))
admin.add_view(BaseMV(Country, db.session))
admin.add_view(BaseMV(ContactUs, db.session))'''


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


##################
# Robots.txt and Sitemap.xml #
##################
@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/opensearch.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])



##################
# error handlers #
##################

@app.errorhandler(404)
def error_404(error):
    return render_template('error/404.html', title = 'Oops!'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('error/500.html', title = 'Server Screwed'), 500
