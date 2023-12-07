from config import SQLALCHEMY_DATABASE_URI
from app import db, app
import os.path

app.app_context().push()

db.create_all()
