from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
logging.basicConfig(filename='record.log', level=logging.DEBUG)

from app import views, models
