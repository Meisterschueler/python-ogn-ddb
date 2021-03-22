from time import time
import jwt
from datetime import datetime
from flask import current_app
from app import db


class DeviceClaim(db.Model):
    __tablename__ = "device_claims"

    id = db.Column(db.Integer, primary_key=True)

    claim_message = db.Column(db.String(255))
    claim_timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    owner_message = db.Column(db.String(255))
    owner_timestamp = db.Column(db.DateTime)

    admin_message = db.Column(db.String(255))
    admin_timestamp = db.Column(db.DateTime)

    is_approved = db.Column(db.Boolean)
    provide_email = db.Column(db.Boolean)

    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    device = db.relationship("Device", backref=db.backref("claims", order_by=claim_timestamp))

    claimer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    claimer = db.relationship("User", foreign_keys=[claimer_id], backref=db.backref("claims_as_claimer", order_by=claim_timestamp))

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", foreign_keys=[owner_id], backref=db.backref("claims_as_owner", order_by=claim_timestamp))

    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    admin = db.relationship("User", foreign_keys=[admin_id], backref=db.backref("claims_ad_admin", order_by=claim_timestamp))

    def get_token(self, expires_in=600):
        return jwt.encode({"device_claim": self.id, "exp": time() + expires_in}, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return DeviceClaim.query.get(payload['device_claim']) if time() <= payload['exp'] else None
        except Exception:
            return None
