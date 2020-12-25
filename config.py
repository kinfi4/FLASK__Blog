import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the_secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1415926535@localhost:5432/kinbook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
