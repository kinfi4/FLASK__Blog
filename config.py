import os

basedir = os.path.abspath(os.path.dirname(__file__))

MEDIA_FOLDER = '/home/kini4/python/MicroBlog/app/media'


class Config:
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the_secret'
    SQLALCHEMY_DATABASE_URI = 'postgres://dboqmuivwekyez:a9df6412863e26d9d695cc60abde9d3cbf7584e89799d90448054b1cf0ed9da9@ec2-107-22-7-9.compute-1.amazonaws.com:5432/dcq4n4r1trc073'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or None

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = 'illuya607@gmail.com'
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

    ADMINS = ['illuya607@gmail.com']
