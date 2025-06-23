# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    zipcode = StringField('Zip Code', validators=[DataRequired(), Length(min=5, max=10)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ListingForm(FlaskForm):
    produce = SelectField('Produce', choices=[], coerce=int, validators=[DataRequired()])
    listing_type = SelectField('Type', choices=[('have', 'Have'), ('want', 'Want')], validators=[DataRequired()])
    submit = SubmitField('Submit Listing')