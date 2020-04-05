from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo, Regexp
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_babel import lazy_gettext as _l
from app.models import AircraftCategory, AircraftType, Antenna, User, DeviceType, Preamplifier, RxFilter, SdrDongle


class LoginForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))


class RegisterForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")])
    password2 = PasswordField(_l("Repeat Password"), validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField(_l("Register"))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        if user is not None:
            raise ValidationError(_l("Please choose a different email address."))


class ChangePasswordForm(FlaskForm):
    email = StringField(_l("Email"), render_kw={"readonly": True})
    old_password = PasswordField(_l("Password"))
    new_password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")])
    new_password2 = PasswordField(_l("Repeat Password"), validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField(_l("Save changes"))

    def validate_old_password(self, old_password):
        user = User.query.filter_by(email=self.email.data).one()
        if not user.check_password(old_password):
            raise ValidationError(_l("Old password is not correct"))


class AddDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), validators=[Regexp("[A-Fa-f0-9]{6}")])
    confirm_ownership = BooleanField(_l("I certify to be the owner of this device"), validators=[DataRequired()])
    submit = SubmitField(_l("Add Device"))


class EditDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), render_kw={"readonly": True})
    device_type = SelectField(_l("Device type"), choices=DeviceType.choices(), coerce=DeviceType.coerce)
    aircraft_category = SelectField(_l("Aircraft category"), choices=AircraftCategory.choices(), coerce=AircraftCategory.coerce)
    aircraft_type = QuerySelectField(_l("Aircraft type"), query_factory=lambda: AircraftType.query)
    registration = StringField(_l("Registration"), validators=[Length(max=7)])
    cn = StringField(_l("CN"), validators=[Length(max=3)])
    show_track = BooleanField(_l("I want this device to be tracked"))
    show_identity = BooleanField(_l("I want this device to be identified"))
    submit = SubmitField(_l("Save changes"))


class ClaimDeviceForm(FlaskForm):
    address = StringField(_l("Device ID"), render_kw={"readonly": True})
    message = TextAreaField(_l("Message"), validators=[DataRequired(), Length(min=0, max=140)])
    provide_email = BooleanField(_l("Provide my email address to the current owner"))
    submit = SubmitField(_l("Submit claim"))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Submit Request"))


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
