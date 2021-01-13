from flask import render_template, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required

from app import app, db
from app.mixins.create_post_mixin import CreatePostMixin
from app.forms import EditProfileForm
from app.models import User, Post
from app.utils.save_picture_into_file_system import save_form_pic


class UserPage(CreatePostMixin, MethodView):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        page = request.args.get('page', 1, type=int)

        posts_for_page = Post.query.filter_by(user_id=user.id).order_by(Post.timespan.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)

        next_page = url_for('user_page', username=username,
                            page=posts_for_page.next_num) if posts_for_page.has_next else None
        prev_page = url_for('user_page', username=username,
                            page=posts_for_page.prev_num) if posts_for_page.has_prev else None

        return render_template('user.html', user=user, posts=posts_for_page.items, next_page=next_page,
                               prev_page=prev_page, **self.mixin_context)


class EditProfile(MethodView):
    @login_required
    def get(self):
        form = EditProfileForm(current_user.username, current_user.email)
        form.name.data = current_user.username
        form.about_me.data = current_user.about_me
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email

        return render_template('forms/edit-profile.html', form=form)

    @login_required
    def post(self):
        form = EditProfileForm(current_user.username, current_user.email)
        if form.validate_on_submit():
            if form.avatar.data:
                current_user.image_file = save_form_pic(form.avatar.data)

            current_user.username = form.name.data
            current_user.about_me = form.about_me.data
            current_user.email = form.email.data
            current_user.full_name = form.full_name.data

            db.session.commit()

            flash('Your changes have been saved.', category='info')
            return redirect(url_for('edit_profile'))
        else:
            return redirect(url_for('/edit_profile', form=form))


app.add_url_rule(rule='/user/<string:username>', view_func=UserPage.as_view('user_page'), methods=['GET', 'POST'])
app.add_url_rule(rule='/edit_profile', view_func=EditProfile.as_view('edit_profile'), methods=['GET', 'POST'])
