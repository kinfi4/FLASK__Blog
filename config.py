import os
from secret import GMAIL_PASSWORD

basedir = os.path.abspath(os.path.dirname(__file__))

MEDIA_FOLDER = '/home/kini4/python/MicroBlog/app/media'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the_secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1415926535@localhost:5432/kinbook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = 'illuya607@gmail.com'
    MAIL_PASSWORD = GMAIL_PASSWORD

    ADMINS = ['illuya607@gmail.com']
