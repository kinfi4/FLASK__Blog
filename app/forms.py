from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField

from app.models import User


class LoginForm(FlaskForm):
    login = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=40)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
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
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=40)])
    name = StringField(label='Name: ', validators=[Length(min=2, max=20)])
    email = StringField(label='Email: ', validators=[Email()])
    avatar = FileField('Update user avatar', validators=[FileAllowed(['jpg', 'png'])])

    about_me = TextAreaField(label='About me:', validators=[Length(max=120)])
    submit = SubmitField('Save')

    def __init__(self, original_name, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_email = original_email

    def validate_name(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.name.data).first()
            if user:
                raise ValidationError('Please use a different username')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(username=self.email.data).first()
            if user:
                raise ValidationError('Please use a different email')


class CreatePostForm(FlaskForm):
    body = TextAreaField(label='Post: ')
    submit = SubmitField('POST')


class EmailForResetPasswordForm(FlaskForm):
    email = StringField(label='Enter your account email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
