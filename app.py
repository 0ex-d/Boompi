#!/usr/bin/env python3
# app.py


"""
Start: 07/25/2017
Written by:
Precious Kindo -- KindoLabs
"""
import os

from flask import Flask, abort
from core import app

app.debug =  app.config['DEBUG']
app.threaded=True

port = int(os.environ.get('PORT',5000))
app.run(host='0.0.0.0', port=port)