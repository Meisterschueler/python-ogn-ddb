import unittest
from unittest.mock import patch
from app import db
from app.models import Device, DeviceClaim, User
from .base import TestCaseBase


class TestClaim(TestCaseBase):
    def get_device_claim(self):
        owner = User(email='klaus@localhost')
        claimer = User(email='kurt@localhost')
        device = Device(user=owner, address='DD1234')
        device_claim = DeviceClaim(device=device, owner=owner, claimer=claimer)
        db.session.add(device_claim)
        db.session.commit()

        self.assertTrue(device_claim.is_approved is None)
        self.assertEqual(device.user, owner)

        return device_claim

    def test_claim_accepted(self):
        device_claim = self.get_device_claim()

        # get device_claim via token and accept the claim
        token = device_claim.get_token()
        device_claim2 = DeviceClaim.verify_token(token)
        self.assertEqual(device_claim, device_claim2)

        with self.app.test_client() as c:
            with patch('app.main.routes.current_user', device_claim.owner):
                response = c.get(f'/claim_accepted/{token}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)

        # check if the claimer is now the new owner of the device
        self.assertTrue(device_claim.is_approved is True)
        self.assertEqual(device_claim.device.user, device_claim.claimer)

    def test_claim_rejected(self):
        device_claim = self.get_device_claim()

        # get device_claim via token and reject the claim
        token = device_claim.get_token()
        device_claim2 = DeviceClaim.verify_token(token)
        self.assertEqual(device_claim, device_claim2)

        with self.app.test_client() as c:
            with patch('app.main.routes.current_user', device_claim.owner):
                response = c.get(f'/claim_rejected/{token}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)

        # check if the owner is still the owner of the device
        self.assertTrue(device_claim.is_approved is False)
        self.assertEqual(device_claim.device.user, device_claim.owner)


if __name__ == "__main__":
    unittest.main()
