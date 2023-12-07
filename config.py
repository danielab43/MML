import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'please-stop-snowing123'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db?check_same_thread=False')
SQLALCHEMY_TRACK_MODIFICATIONS = True
