from datetime import datetime, time, timedelta

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from app import db, login, app

from config import MEDIA_FOLDER
from app.utils.get_passed_time import get_time_format
from app.mixins.searchable_mixin import SearchableMixin


@login.user_loader
def login_user(id_):
    return User.query.get(int(id_))


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    image_file = db.Column(db.String(30), default='default.jpg')

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy=True)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self, size=32):
        return url_for('static', filename='media/users_avatars/' + self.image_file)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    @property
    def followed_posts(self):
        followed = Post.query.join(
            followers, (Post.user_id == followers.c.followed_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)

        return followed.union(own).order_by(Post.timespan.desc())

    @property
    def get_last_seen(self):
        return get_time_format(self.last_seen)

    @property
    def posts_number(self):
        return len(self.posts)

    def get_reset_password_token(self, token_time_available=600):
        return jwt.encode({
            'reset_password': self.id, 'exp': datetime.now() + timedelta(seconds=token_time_available)},
            app.config['SECRET_KEY'],
            algorithm='HS256').encode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'User: {self.username}'


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(length=300))
    timespan = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            'user_id': self.user_id,
            'body': self.body,
            'timespan': self.timespan
        }

    @property
    def post_date(self):
        return get_time_format(self.timespan)

    def __repr__(self):
        return f'{self.author.username}: {self.body}'
