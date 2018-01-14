#!/usr/bin/env python3

import os
import sys
import string
import random

from flask import *

from core import *
from core.models import *
from core.users.models import *
from core.tracks.models import *

from core.utils import slugify

#env = os.environ.get('APP_ENV')
env = "development"
app.config.from_object('config.%sConfig' % env.capitalize())

def id_gen(size=6):
    chars=string.digits
    return ''.join(random.choice(chars) for x in range(size))

db.drop_all()
db.create_all()

# Country
print("Creating **Country** table ---------")
ctry = Country(1, 'NG', 'Nigeria', '234')
db.session.add(ctry)
db.session.commit()

# User
print("\n\nCreating **Role** table ---------")
role_1 = Role(5, 'moderator', 'Moderator')
role_2 = Role(6, 'admin', 'Administrator')
role_3 = Role(2, 'user', 'End user')
role_4 = Role(4, 'staff', 'Staff')

db.session.add(role_1)
db.session.add(role_2)
db.session.add(role_3)
db.session.add(role_4)
db.session.commit()

# User
print("Creating **User** table ---------")
bot = User(
	email="jbott@boompi.com",
	fullname='Jimmy Bot',
	username='jbott',
	phone='',
	avatar='',
	password='test@v1'
)

user = User(
	email="david@gmail.com", 
	fullname='David Ikomi',
	username='davekomi924',
	phone='234809566545',
	avatar='',
	password='david'
)

user1 = User(
	email="steve_o@gmail.com", 
	fullname='Steve Crown',
	username='steve_o',
	phone='234805643422',
	avatar='steve_o.jpg',
	password='david'
)

user2 = User(
	email="frank@gmail.com", 
	fullname='Frank Edwards',
	username='franky_ed',
	phone='',
	avatar='franky_ed.jpg',
	password='david'
)

user3 = User(
	email="panam@gmail.com", 
	fullname='Panam Percy Paul',
	username='panam_percy',
	phone='',
	avatar='panam_percy.jpg',
	password='david'
)

db.session.add(bot)
db.session.add(user)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# Append Roles
# mod = 1, staff = 3, admin = 6

print("Assigning **Roles** to users ---------")
user_datastore.add_role_to_user('david@gmail.com', 'admin')
db.session.commit()

# Profile
print("Creating **Profile** table ---------")
user_p = Profile(id=user.id, country_id=1)
user_p1 = Profile(id=user1.id, country_id=1, is_artist=True)
user_p2 = Profile(id=user2.id, country_id=1, is_artist=True)
user_p3 = Profile(id=user3.id, country_id=1, is_artist=True)
db.session.add(user_p)
db.session.add(user_p1)
db.session.add(user_p2)
db.session.add(user_p3)
db.session.commit()

# Genre
print("Creating **Genres** table ---------")
gnr = Genre(1, 'Gospel')
db.session.add(gnr)
db.session.commit()

# Tag
print("Creating **Tags** table ---------")
tg = Tag('Africa')
tg1 = Tag('Yoruba')
tg2 = Tag('America')
tg3 = Tag('Igbo')
tg4 = Tag('Worship')
db.session.add(tg)
db.session.add(tg1)
db.session.add(tg2)
db.session.add(tg3)
db.session.add(tg4)
db.session.commit()

# Track
print("Creating **Tracks** table ---------")
trck = Track(title='I Will Follow You', media='I_Will_Follow_You.mp3', artwork='I_Will_Follow_You.jpg', user_id=user3.id, slug=slugify('I Will Follow You'))
trck1 = Track(title='You Are Great', media='You_Are_Great.mp3', artwork='You_Are_Great.jpg', user_id=user1.id, slug=slugify('You Are Great'))
db.session.add(trck)
db.session.add(trck1)
db.session.commit()

# TrackStats
print("Creating **TrackStats** table ---------")
trckst = TrackStats(trck.id)
trckst1 = TrackStats(trck1.id)
db.session.add(trckst)
db.session.add(trckst1)
db.session.commit()