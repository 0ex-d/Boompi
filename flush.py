#!/usr/bin/env python3

import os
import sys
import string
import random

from flask import *
from werkzeug import check_password_hash, generate_password_hash

from core import *
from core.models import *
from core.users.models import *
#from core.tracks.models import *

#env = os.environ.get('APP_ENV')
env = "development"
app.config.from_object('config.%sConfig' % env.capitalize())

def id_gen(size=6):
    chars=string.digits
    return ''.join(random.choice(chars) for x in range(size))

db.drop_all()

print("\n\nAll Tables flushed ---------")

db.create_all()

print("\n\nAll Tables rebuilt ---------")