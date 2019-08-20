import unittest
from app import app, db
from tests.utils import build_db_from_ddb
from app.models import Device


class TestDB(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self):
        #db.session.remove()
        #db.drop_all()
        pass

    def test_wtf(self):
        build_db_from_ddb()
        devices = db.session.query(Device).all()
        print(devices)

unittest.main()