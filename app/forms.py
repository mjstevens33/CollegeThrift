from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, NumberRange
from app.models import User
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')


    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('An account already exists with this email')

    def validate_userName(self, username):
        user = User.query.filter_by(email=username.data).first()
        if user is not None:
            raise ValidationError('An account already exists with this username')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Item')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Add Item')