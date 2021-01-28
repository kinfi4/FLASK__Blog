import os

basedir = os.path.abspath(os.path.dirname(__file__))

MEDIA_FOLDER = '/home/kini4/python/MicroBlog/app/media'


class Config:
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the_secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1415926535@localhost:5432/kinbook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = 'illuya607@gmail.com'
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

    ADMINS = ['illuya607@gmail.com']
