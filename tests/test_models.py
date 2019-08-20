import unittest
from app.models import Device, User


class TestModels(unittest.TestCase):
    def test_user_password(self):
        user = User()
        password = "my_secret"
        user.set_password(password)

        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password("bad_guess"))

    def test_user_device_relationship(self):
        user = User()
        device = Device()
        user.followed_devices.append(device)
        
        self.assertTrue(user in device.following_users)
        self.assertTrue(device in user.followed_devices)
        
if __name__ == '__main__':
    unittest.main()
