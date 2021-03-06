from time import time
import jwt
from crypt import crypt
from flask import current_app
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    is_activated = db.Column(db.Boolean, nullable=False, default=False)

    followed_devices = db.relationship("Device", secondary="association_table_users_devices", back_populates="following_users")
    followed_receivers = db.relationship("Receiver", secondary="association_table_users_receivers")

    def set_password(self, password):
        self.password_hash = crypt(password, current_app.config["OGN_SECRET_KEY"])

    def check_password(self, password):
        return crypt(password, current_app.config["OGN_SECRET_KEY"]) == self.password_hash

    def __str__(self):
        return self.email

    def __repr__(self):
        return "User(email={self.email})".format(self=self)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id, "exp": time() + expires_in}, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    def get_account_activation_token(self, expires_in=600):
        return jwt.encode({"account_activation": self.id, "exp": time() + expires_in}, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def verify_password_token(token):
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return User.query.get(payload['reset_password']) if time() <= payload['exp'] else None
        except Exception:
            return None

    @staticmethod
    def verify_account_activation_token(token):
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return User.query.get(payload['account_activation']) if time() <= payload['exp'] else None
        except Exception:
            return None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
