from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from flask.views import MethodView

from app import app, db
from app.forms import CreatePostForm
from app.models import Post


class CreatePost(MethodView):
    @login_required
    def get(self):
        return render_template('forms/create-post.html', **self.prepare_context())

    @staticmethod
    def prepare_context():
        return {
            'form': CreatePostForm(),
            'form_endpoint': url_for('create_post')
        }

    @login_required
    def post(self):
        form = CreatePostForm()
        post = Post()

        if form.validate_on_submit():
            post.user_id = current_user.id
            post.body = form.body.data

            db.session.add(post)
            db.session.commit()

        return redirect(url_for('user_page', username=current_user.username))


@app.route('/delete_post/<id_>', methods=['POST'])
@login_required
def delete_post(id_):
    post = Post.query.filter_by(user_id=current_user.id).filter_by(id=id_).first()
    if not post:
        abort(405)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_page', username=current_user.username))


@app.route('/edit_post/<id_>', methods=['GET', 'POST'])
def edit_post(id_):
    form = CreatePostForm()
    post = Post.query.filter_by(user_id=current_user.id).filter_by(id=id_).first()

    if not post:
        abort(405)

    if request.method == 'POST':
        if form.validate_on_submit():
            post.body = form.body.data

            db.session.commit()
        else:
            flash('Form was not edited, something wrong!', category='error')

        return redirect(url_for('user_page', username=current_user.username))
    elif request.method == 'GET':
        form.body.data = post.body

        context = {
            'form': form,
            'title': 'Edit post',
            'form_endpoint': url_for('edit_post', id_=post.id)
        }

        return render_template('forms/create-post.html', **context)


app.add_url_rule('/create-post', view_func=CreatePost.as_view('create_post'), methods=['GET', 'POST'])
