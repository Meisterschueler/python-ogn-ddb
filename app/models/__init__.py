# flake8: noqa

from app import db

from .antenna import Antenna
from .aircraft_type import AircraftType
from .aircraft_category import AircraftCategory
from .user import User
from .device import Device
from .device_type import DeviceType
from .device_claim import DeviceClaim
from .preamplifier import Preamplifier
from .receiver import Receiver
from .rx_filter import RxFilter
from .sdr_dongle import SdrDongle


class UsersDevices(db.Model):
    __tablename__ = "association_table_users_devices"

    user__id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), primary_key=True)


class UsersReceivers(db.Model):
    __tablename__ = "association_table_users_receivers"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey("receivers.id"), primary_key=True)
