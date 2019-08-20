from app import db
from .device_type import DeviceType


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String(6), nullable=False)
    device_type = db.Column(db.Enum(DeviceType))
    registration = db.Column(db.String(7))
    cn = db.Column(db.String(3))
    show_track = db.Column(db.Boolean, nullable=False, default=True)
    show_identity = db.Column(db.Boolean, nullable=False, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref="devices")

    aircraft_type_id = db.Column(db.Integer, db.ForeignKey("aircraft_types.id"))
    aircraft_type = db.relationship("AircraftType", backref="devices")

    following_users = db.relationship("User", secondary="association_table_users_devices", back_populates="followed_devices")

    def __repr__(self):
        return "Device(address={self.address}, registration={self.registration}, cn={self.cn})".format(self=self)
