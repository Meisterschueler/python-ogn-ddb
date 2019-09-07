import unittest
from app import create_app, db
from app.fake import build_db_from_ddb
from app.models import Device


class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_wtf(self):
        build_db_from_ddb()
        devices = db.session.query(Device).all()
        print(devices)


if __name__ == "__main__":
    unittest.main()
