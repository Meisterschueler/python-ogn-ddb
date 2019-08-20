from datetime import datetime
from app import db


class DeviceClaim(db.Model):
    __tablename__ = "device_claims"

    id = db.Column(db.Integer, primary_key=True)

    request_message = db.Column(db.String(255), nullable=False)
    request_timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    respond_message = db.Column(db.String(255))
    respond_timestamp = db.Column(db.DateTime)

    is_approved = db.Column(db.Boolean)

    # device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    # device = db.relationship('Device', backref=db.backref('claims', order_by=request_timestamp))

    # owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # owner = db.relationship('User', primaryjoin=[owner_id], backref=db.backref('claims', order_by=request_timestamp))

    # requestor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # requestor = db.relationship('User', primaryjoin=[requestor_id], backref=db.backref('requested_claims', order_by=request_timestamp))

    # responder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # responder = db.relationship('User', primaryjoin=[responder_id], backref=db.backref('responded_claims', order_by=request_timestamp))
