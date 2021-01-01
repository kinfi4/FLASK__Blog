import unittest
from datetime import datetime, timedelta

from app import db, app
from app.models import User, Post


class TestUserModel(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        password = 'UWillNeverGuess'

        u.set_password_hash(password)
        self.assertFalse(u.check_password('RandomPassword'))
        self.assertTrue(u.check_password(password))

    def test_follow(self):
        u1 = User(username='Tom', email='Tom@gmail.com')
        u2 = User(username='Sam', email='San@gmail.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Sam')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)

    def test_get_followed_posts(self):
        u1 = User(username='Tom', email='name@gmail.com')
        u2 = User(username='Sam', email='sam@gmail.com')
        u3 = User(username='John', email='john@gmail.com')
        u4 = User(username='Lucy', email='lucy@gmail.com')

        db.session.add_all((u1, u2, u3, u4))
        db.session.commit()

        now = datetime.now()
        p1 = Post(
            user_id=1, body='post from tom',
            timespan=now + timedelta(seconds=1))

        p2 = Post(
            user_id=2, body='post from sam',
            timespan=now + timedelta(seconds=4)
        )

        p3 = Post(
            user_id=3, body='post from john',
            timespan=now + timedelta(seconds=2)
        )

        p4 = Post(
            user_id=4, body='post from lucy',
            timespan=now + timedelta(seconds=3)
        )

        db.session.add_all((p1, p2, p3, p4))
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u2.follow(u1)
        u2.follow(u4)
        u3.follow(u4)
        db.session.commit()

        posts1 = u1.followed_posts.all()
        posts2 = u2.followed_posts.all()
        posts3 = u3.followed_posts.all()
        posts4 = u4.followed_posts.all()

        self.assertEqual(posts1, [p1, p3, p2])
        self.assertEqual(posts2, [p1, p4, p2])
        self.assertEqual(posts3, [p3, p4])
        self.assertEqual(posts4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
