from datetime import datetime
import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
from werkzeug.urls import url_parse
from app import db
from app.main.forms import RegisterForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm, AddDeviceForm, EditDeviceForm, ClaimDeviceForm, EditReceiverForm
from app.models import AircraftCategory, AircraftType, Device, DeviceClaim, User, Receiver
from app.main import bp
from app.emails import send_password_reset_email, send_account_activation_email, send_device_claim_email


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html", title=_("Home"))


@bp.route("/my_devices")
@login_required
def my_devices():
    devices = Device.query.filter(db.or_(Device.user == current_user, Device.following_users.contains(current_user))).all()
    return render_template("devices.html", title=_("Devices"), devices=devices)


@bp.route("/all_devices")
def all_devices():
    devices = Device.query.all()
    return render_template("devices.html", title=_("Devices"), devices=devices)


@bp.route("/my_receivers")
@login_required
def my_receivers():
    receivers = current_user.receivers
    return render_template("receivers.html", title=_("Receivers"), receivers=receivers)


@bp.route("/all_receivers")
def all_receivers():
    receivers = Receiver.query.all()
    return render_template("receivers.html", title=_("Receivers"), receivers=receivers)


@bp.route("/edit_receiver", methods=["GET", "POST"])
@login_required
def edit_receiver():
    receiver_id = request.args.get("receiver_id")
    receiver = Receiver.query.filter_by(id=receiver_id).first_or_404()

    form = EditReceiverForm()
    if form.validate_on_submit():
        receiver.name = form.name.data
        receiver.description = form.description.data
        receiver.antenna = form.antenna.data
        receiver.preamplifier = form.preamplifier.data
        receiver.rx_filter = form.rx_filter.data
        receiver.sdr_dongle = form.sdr_dongle.data
        db.session.commit()
        return redirect(url_for("main.my_receivers"))
    elif request.method == "GET":
        form.name.data = receiver.name
        form.description.data = receiver.description
        form.antenna.data = receiver.antenna
        form.preamplifier.data = receiver.preamplifier
        form.rx_filter.data = receiver.rx_filter
        form.sdr_dongle.data = receiver.sdr_dongle
    return render_template("form_generator.html", title=_("Edit Receiver"), form=form)


@bp.route("/downloads")
def downloads():
    return render_template("downloads.html", title=_("Downloads"))


@bp.route("/about")
def about():
    return render_template("about.html", title=_("About"))


@bp.route("/user")
@login_required
def user():
    return render_template("user.html", title=_("User"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, is_activated=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        send_account_activation_email(user)

        flash(_("An email has just been sent to you, you'll find instructions on how to validate your account."))
        return redirect(url_for("main.index"))

    return render_template("form_generator.html", title=_("Register"), form=form)


@bp.route("/account_activation/<token>", methods=["GET", "POST"])
def account_activation(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.verify_account_activation_token(token)
    if not user:
        return redirect(url_for("main.index"))

    if not user.is_activated:
        user.is_activated = True
        db.session.commit()
        flash(_("Your account is activated, now you can login."), category='success')
    else:
        flash(_("Your account is already activated."), category='warning')
    return redirect(url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid email address or password"))
            return redirect(url_for("main.login"))
        elif not user.is_activated:
            flash(_("User not activated yet"))
            return redirect(url_for("main.login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("form_generator.html", title=_("Login"), form=form)


@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for("main.index"))


@bp.route("/request_password_reset", methods=["GET", "POST"])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user:
            send_password_reset_email(user)

        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("main.login"))

    return render_template("form_generator.html", title=_("Request Password Reset"), form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Your password has been reset."))
        return redirect(url_for("main.login"))
    return render_template("form_generator.html", title=_("Reset Password"), form=form)


@bp.route("/add_device", methods=["GET", "POST"])
@login_required
def add_device():
    form = AddDeviceForm()
    if form.validate_on_submit():
        address = form.address.data.upper()
        device = Device.query.filter_by(address=address).one_or_none()
        if device is None:
            device = Device(address=address, user=current_user)
            db.session.commit()
            return redirect(url_for("main.edit_device", device_id=device.id))

        else:
            if device.user == current_user:
                flash(_("You already own this device"), category="warning")
                return redirect(url_for("main.my_devices"))
            else:
                device_claim = DeviceClaim.query.\
                    filter_by(device_id=device.id).\
                    filter_by(claimer=current_user).one_or_none()
                if device_claim is None:
                    flash(_("This device is used by another user"), category="danger")
                    return redirect(url_for("main.claim_device", device_id=device.id))
                else:
                    flash(_("This device is used by another user, but you already opened a claim"))
                    return redirect(url_for("main.my_devices"))

    return render_template("form_generator.html", title=_("Add Device"), form=form)


@bp.route("/edit_device", methods=["GET", "POST"])
@login_required
def edit_device():
    device_id = request.args.get("device_id")
    device = Device.query.filter_by(id=device_id).filter_by(user_id=current_user.id).first_or_404()

    form = EditDeviceForm()

    aircraft_data = {}
    for category in AircraftCategory:
        aircraft_types = [(at.id, at.name) for at in AircraftType.query.filter_by(category=category).order_by(AircraftType.name)]
        aircraft_data[category.name] = aircraft_types

    if form.validate_on_submit():
        device.device_type = form.device_type.data
        device.aircraft_type_id = form.aircraft_type.data.id
        device.registration = form.registration.data.upper()
        device.cn = form.cn.data.upper()
        device.show_track = form.show_track.data
        device.show_identity = form.show_identity.data
        db.session.commit()
        return redirect(url_for("main.my_devices"))
    elif request.method == "GET":
        form.address.data = device.address
        form.device_type.data = device.device_type
        form.registration.data = device.registration
        form.cn.data = device.cn
        form.show_track.data = device.show_track
        form.show_identity.data = device.show_identity

    return render_template(
        "form_edit_device.html",
        title=_("Edit Device"),
        form=form,
        aircraft_data=json.dumps(aircraft_data),
        aircraft_type=device.aircraft_type)


@bp.route("/delete_device", methods=["GET", "POST"])
@login_required
def delete_device():
    device_id = request.args.get("device_id")
    device = Device.query.filter_by(id=device_id).filter_by(user_id=current_user.id).first_or_404()
    db.session.delete(device)
    db.session.commit()

    return redirect(url_for("main.my_devices"))


@bp.route("/follow_device/<device_id>", methods=["GET", "POST"])
@login_required
def follow_device(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()
    if current_user not in device.following_users:
        device.following_users.append(current_user)
        db.session.commit()

    return "success", 200


@bp.route("/unfollow_device/<device_id>", methods=["GET", "POST"])
@login_required
def unfollow_device(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()
    if current_user in device.following_users:
        device.following_users.remove(current_user)
        db.session.commit()

    return "success", 200


@bp.route("/claim_device", methods=["GET", "POST"])
@login_required
def claim_device():
    device_id = request.args.get("device_id")
    device = Device.query.filter_by(id=device_id).first_or_404()

    form = ClaimDeviceForm()
    if form.validate_on_submit():
        device_claim = DeviceClaim()
        device_claim.claim_message = form.message.data
        device_claim.device = device
        device_claim.owner = device.user
        device_claim.claimer = current_user
        device_claim.provide_email = form.provide_email.data
        db.session.commit()

        send_device_claim_email(device_claim)

        flash(_("Claim successfully commited"), category="success")

        return redirect(url_for("main.my_devices"))

    form.address.data = device.address
    return render_template("form_generator.html", title=_("Claim Device Ownership"), form=form)


@bp.route("/claim_accepted/<token>", methods=["GET", "POST"])
@login_required
def claim_accepted(token):
    device_claim = DeviceClaim.verify_token(token)
    if not device_claim or device_claim.owner != current_user:
        return redirect(url_for("main.index"))

    device_claim.owner_timestamp = datetime.utcnow()
    device_claim.owner_message = f"accepted with token {token}"

    device_claim.is_approved = True
    device_claim.device.user = device_claim.claimer

    db.session.commit()
    flash(_("Claim accepted."), category="success")

    return redirect(url_for("main.index"))


@bp.route("/claim_rejected/<token>", methods=["GET", "POST"])
@login_required
def claim_rejected(token):
    device_claim = DeviceClaim.verify_token(token)
    if not device_claim or device_claim.owner != current_user:
        return redirect(url_for("main.index"))

    device_claim.owner_timestamp = datetime.utcnow()
    device_claim.owner_message = f"rejected with token {token}"

    device_claim.is_approved = False

    db.session.commit()
    flash(_("Claim rejected."), category="success")

    return redirect(url_for("main.index"))
