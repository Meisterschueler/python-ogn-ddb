from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
from werkzeug.urls import url_parse
from app import db
from app.main.forms import RegisterForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm, AddDeviceForm, EditDeviceForm, ClaimDeviceForm, EditReceiverForm
from app.models import AircraftType, User, Device, Receiver
from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html", title=_("Home"))


@bp.route("/my_devices")
@login_required
def my_devices():
    devices = current_user.devices
    return render_template("devices.html", title=_("Devices"), devices=devices)


@bp.route("/all_devices")
def all_devices():
    devices = Device.query.all()
    return render_template("devices.html", title=_("Devices"), devices=devices)


@bp.route("/my_receivers")
@login_required
def my_receivers():
    return render_template("receivers.html", title=_("Receivers"))


@bp.route("/all_receivers")
def all_receivers():
    return render_template("receivers.html", title=_("Receivers"))


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


@bp.route("/aircraft_types")
def aircraft_types():
    aircraft_types = AircraftType.query.order_by(AircraftType.category, AircraftType.name).all()
    return render_template("aircraft_types.html", title=_("Aircraft Types"), aircraft_types=aircraft_types)


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


@bp.route("/claims")
@login_required
def claims():
    return render_template("user.html", title=_("Claims"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Congratulations! You are now a registered user."))
        return redirect(url_for("main.index"))

    return render_template("form_generator.html", title=_("Register"), form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid email address or password"))
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
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # send email
            pass

        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("main.login"))

    return render_template("form_generator.html", title=_("Request Password Reset"), form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.verify_password_token(token)
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
        device = Device.query.filter_by(address=address).first()
        if device is not None:
            if device.user == current_user:
                flash(_("You already own this device"), category="warning")
                return redirect(url_for("main.my_devices"))
            else:
                flash(_("This device is used by another user"), category="danger")
                return redirect(url_for("main.claim_device", device_id=device.id))
        else:
            device = Device(address=address, user=current_user)
            db.session.commit()
            return redirect(url_for("main.edit_device", device_id=device.id))

    return render_template("form_generator.html", title=_("Add Device"), form=form)


@bp.route("/edit_device", methods=["GET", "POST"])
@login_required
def edit_device():
    device_id = request.args.get("device_id")
    device = Device.query.filter_by(id=device_id).filter_by(user_id=current_user.id).first_or_404()

    form = EditDeviceForm()
    form.aircraft_type_id.choices = AircraftType.choices()

    if form.validate_on_submit():
        device.device_type = form.device_type.data
        device.aircraft_type_id = form.aircraft_type_id.data
        device.registration = form.registration.data.upper()
        device.cn = form.cn.data.upper()
        device.show_track = form.show_track.data
        device.show_identity = form.show_identity.data
        db.session.commit()
        return redirect(url_for("main.my_devices"))
    elif request.method == "GET":
        form.address.data = device.address
        form.device_type.data = device.device_type
        form.aircraft_type_id.data = device.aircraft_type_id
        form.registration.data = device.registration
        form.cn.data = device.cn
        form.show_track.data = device.show_track
        form.show_identity.data = device.show_identity

    return render_template("form_generator.html", title=_("Edit Device"), form=form)


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
        pass

    form.address.data = device.address
    return render_template("form_generator.html", title=_("Claim Device Ownership"), form=form)
