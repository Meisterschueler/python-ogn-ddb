from app import db
from .antenna import Antenna
from .preamplifier import Preamplifier
from .rx_filter import RxFilter
from .sdr_dongle import SdrDongle


class Receiver(db.Model):
    __tablename__ = "receivers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(9))
    description = db.Column(db.String(255))
    antenna = db.Column(db.Enum(Antenna))
    preamplifier = db.Column(db.Enum(Preamplifier))
    rx_filter = db.Column(db.Enum(RxFilter))
    sdr_dongle = db.Column(db.Enum(SdrDongle))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="receivers")

    following_users = db.relationship("User", secondary="association_table_users_receivers")

    def __repr__(self):
        return "Receiver(antenna={self.antenna}, preamplifier={self.preamplifier}, rx_filter={self.rx_filter}, sdr_dongle={self.sdr_dongle})".format(self=self)
