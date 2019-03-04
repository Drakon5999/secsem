# -*- coding: utf-8 -*-

try:
    from secrets import token_hex  # For python 3.6 and higher
except ImportError:
    from os import urandom  # For python less than 3.6


    def token_hex(nbytes=None):
        return urandom(nbytes).hex()

from flask import Flask, session, g
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
SECRET_KEY = token_hex(16)
SESSION_TYPE = 'filesystem'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE
app.secret_key = SECRET_KEY
DATABASE = "landing/site.db"
sess = Session()

from landing import routes
