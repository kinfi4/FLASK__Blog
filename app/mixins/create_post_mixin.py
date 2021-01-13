from flask_login import current_user
from flask import redirect, url_for

from app import db
from app.forms import CreatePostForm
from app.models import Post


class CreatePostMixin:
    def post(self, username=None):
        form = CreatePostForm()
        post = Post()

        if form.validate_on_submit():
            post.user_id = current_user.id
            post.body = form.body.data

            db.session.add(post)
            db.session.commit()

        return redirect(url_for('user_page', username=current_user.username))

    @property
    def mixin_context(self):
        return {
            'form': CreatePostForm()
        }
