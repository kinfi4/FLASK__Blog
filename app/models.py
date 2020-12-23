from hashlib import md5
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

from app.constants import MAX_POST_LENGTH, months


@login.user_loader
def login_user(id_):
    return User.query.get(int(id_))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime, default=datetime.now())

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @property
    def get_last_seen(self):
        time_past = datetime.now() - self.last_seen

        if time_past < timedelta(minutes=1):
            return f'{time_past.seconds}s ago'

        elif time_past < timedelta(hours=1):
            return f'{time_past.seconds // 60}m ago'

        elif time_past < timedelta(days=1):
            return f'{time_past.seconds // 3600}h ago'

        elif time_past < timedelta(days=365):
            return f' on {months.get(self.timespan.month, "undefined")} {self.timespan.day}'
        else:
            return f' on {self.timespan.year} {months.get(self.timespan.month, "undefined")} {self.timespan.day}'

    def __repr__(self):
        return f'User: {self.username}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(length=10e4))
    timespan = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def author(self):
        return User.query.filter_by(id=self.user_id).first()

    @property
    def post_date(self):
        time_past = datetime.now() - self.timespan

        if time_past < timedelta(minutes=1):
            return f'{time_past.seconds}s'

        elif time_past < timedelta(hours=1):
            return f'{time_past.seconds // 60}m'

        elif time_past < timedelta(days=1):
            return f'{time_past.seconds // 3600}h'

        elif time_past < timedelta(days=365):
            return f'{months.get(self.timespan.month, "undefined")} {self.timespan.day}'
        else:
            return f'{self.timespan.year} {months.get(self.timespan.month, "undefined")} {self.timespan.day}'

    def __repr__(self):
        return f'{self.author.username}: {self.body}'

