# app/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectMultipleField,
    SubmitField, DateField, PasswordField)
from wtforms.fields import TelField, EmailField
from wtforms.validators import DataRequired, Email, Length
from datetime import date
from wtforms import ValidationError


class BookingForm(FlaskForm):
    customer_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    phone = TelField(
        "Phone Number",
        validators=[DataRequired(), Length(min=10, max=11)]
    )
    email = EmailField(
        "Email Address",
        validators=[Email(), DataRequired()],
        filters=[lambda x: x or None]
    )
    vehicle_model = StringField("Vehicle Model", validators=[DataRequired()])
    registration_no = StringField("Registration No.")
    date = DateField("Preferred Date", format="%Y-%m-%d", validators=[DataRequired()])
    time_slot = StringField("Preferred Time", validators=[DataRequired()])
    services = SelectMultipleField(
        "Select Services",
        coerce=int,
        validators=[DataRequired()]
)
    notes = TextAreaField("Notes")
    submit = SubmitField("Book Service")

    def validate_date(self, field):
        if field.data < date.today():
            raise ValidationError("Date cannot be in the past")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[Email(), DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Send")


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
