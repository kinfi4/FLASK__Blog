from flask import render_template, request, url_for, redirect, g
from flask_login import current_user
from flask.views import MethodView

from app import app, db
from app.mixins.create_post_mixin import CreatePostMixin
from app.models import Post


class Posts(CreatePostMixin, MethodView):
    def get(self):
        filters = request.args.get('sort_by', 'world')
        page = request.args.get('page', 1, type=int)

        if filters == 'world':
            posts_for_page = Post.query.order_by(Post.timespan.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        elif filters == 'following':
            posts_for_page = current_user.followed_posts.order_by(Post.timespan.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        else:
            posts_for_page = Post.query.order_by(Post.timespan.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)

        next_page = url_for('posts', page=posts_for_page.next_num) if posts_for_page.has_next else None
        prev_page = url_for('posts', page=posts_for_page.prev_num) if posts_for_page.has_prev else None

        return render_template('posts.html', title='Home', posts=posts_for_page.items, next_page=next_page,
                               prev_page=prev_page, form=self.mixin_context.get('form'))


class Search(MethodView):
    def get(self):
        if not g.search_form.validate():
            return redirect(url_for('posts'))

        page = request.args.get('page', 1, type=int)
        posts, total = Post.search(g.search_form.q.data, page, app.config['POSTS_PER_PAGE'])

        next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
            if total > page * app.config['POSTS_PER_PAGE'] else None

        prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
            if page > 1 else None

        return render_template('search.html', title='Search', posts=posts,
                               next_url=next_url, prev_url=prev_url)


app.add_url_rule('/explore', view_func=Posts.as_view('posts'))
app.add_url_rule('/search', view_func=Search.as_view('search'))
