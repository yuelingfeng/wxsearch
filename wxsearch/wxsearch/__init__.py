"""
The flask application package.
"""
from .exts import db
from .db_scripts import dbmanage
from flask import Flask
from .models import Users
from . import configs

app = Flask(__name__)
app.config.from_object(configs)

db.init_app(app)

import wxsearch.views
