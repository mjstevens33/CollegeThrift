from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField, SelectMultipleField, DecimalField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_email(selfself, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('An account already exists with this email')


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Item')