from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField

from app.models import User
from app.constants import MAX_POST_LENGTH


class LoginForm(FlaskForm):
    login = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, *args):
        if User.query.filter_by(username=self.username.data).first() is not None:
            raise ValidationError('Please enter different username')

    def validate_email(self, *args):
        if User.query.filter_by(email=self.email.data).first() is not None:
            raise ValidationError('User with such email already exists')


class EditProfileForm(FlaskForm):
    name = StringField(label='Name: ', validators=[Length(min=2, max=20)])
    about_me = TextAreaField(label='About me:', validators=[Length(min=0, max=200)])
    submit = SubmitField('Save')

    def __init__(self, original_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.name.data).first()
            if user:
                raise ValidationError('Please use a different username')


class CreatePostForm(FlaskForm):
    body = TextAreaField(label='Post: ')
    submit = SubmitField('POST')
