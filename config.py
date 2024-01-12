import os
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "youllnevaguess"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    JWT_SECRET_KEY=os.environ.get('SECRET_KEY') or "youllnevaguess"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)