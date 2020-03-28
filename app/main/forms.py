from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo, Regexp
from flask_babel import lazy_gettext as _l
from app.models import Antenna, User, DeviceType, Preamplifier, RxFilter, SdrDongle


class LoginForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class RegisterForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")])
    password2 = PasswordField(_l("Repeat Password"), validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField(_l("Register"))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l("Please choose a different email address."))


class AddDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), validators=[Regexp("[A-Fa-f0-9]{6}")])
    confirm_ownership = BooleanField(_l("I certify to be the owner of this device"), validators=[DataRequired()])
    submit = SubmitField(_l("Add Device"))


class EditDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), render_kw={"readonly": True})
    device_type = SelectField(_l("Device type"), choices=DeviceType.choices(), coerce=DeviceType.coerce)
    aircraft_type_id = SelectField(_l("Aircraft type"), choices=[], coerce=int)
    registration = StringField(_l("Registration"), validators=[Length(max=7)])
    cn = StringField(_l("CN"), validators=[Length(max=3)])
    show_track = BooleanField(_l("I want this device to be tracked"))
    show_identity = BooleanField(_l("I want this device to be identified"))
    submit = SubmitField(_l("Save changes"))


class ClaimDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), render_kw={"readonly": True})
    message = TextAreaField(_l("Message"), validators=[DataRequired(), Length(min=0, max=140)])
    publish_email = BooleanField(_l("Send my email address"))
    submit = SubmitField(_l("Submit claim"))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Request Password Reset"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")])
    password2 = PasswordField(_l("Repeat Password"), validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField(_l("Reset Password"))


class EditReceiverForm(FlaskForm):
    name = StringField(_l("Name"))
    description = TextAreaField(_l("Description"), validators=[Length(min=0, max=255)])
    antenna = SelectField(_l("Antenna"), choices=Antenna.choices(), coerce=Antenna.coerce)
    preamplifier = SelectField(_l("Preamplifier"), choices=Preamplifier.choices(), coerce=Preamplifier.coerce)
    rx_filter = SelectField(_l("Filter"), choices=RxFilter.choices(), coerce=RxFilter.coerce)
    sdr_dongle = SelectField(_l("SDR Dongle"), choices=SdrDongle.choices(), coerce=SdrDongle.coerce)
    submit = SubmitField(_l("Save Changes"))
