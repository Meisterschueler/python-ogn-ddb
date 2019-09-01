import os
import csv
from app import db
from app.models import Antenna, AircraftType, AircraftCategory, User, Device, DeviceType, Preamplifier, Receiver, RxFilter, SdrDongle


mypath = os.path.dirname(os.path.realpath(__file__))


def build_db_from_ddb():
    user = User(email="user1@email.com")
    user.set_password("topsecret")
    db.session.add(user)

    with open(os.path.join(mypath, "ddb.txt")) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        i = 0
        for row in csvreader:
            i += 1
            device_type = {"F": DeviceType.FLARM, "I": DeviceType.ICAO, "O": DeviceType.OGN}[row["#DEVICE_TYPE"]]
            address = row["DEVICE_ID"]
            aircraft_type_name = row["AIRCRAFT_MODEL"]
            registration = row["REGISTRATION"]
            cn = row["CN"]
            show_track = row["TRACKED"] == "Y"
            show_identity = row["IDENTIFIED"] == "Y"
            aircraft_category = AircraftCategory.coerce(row["AIRCRAFT_TYPE"])

            aircraft_type = AircraftType.query.filter_by(name=aircraft_type_name).first()
            if not aircraft_type:
                aircraft_type = AircraftType(name=aircraft_type_name, category=aircraft_category)

            Device(device_type=device_type, aircraft_type=aircraft_type, address=address, registration=registration, cn=cn, show_track=show_track, show_identity=show_identity, user=user)

            if i == 1000:
                break

        db.session.commit()


def build_db():
    a1 = AircraftType(name="ASH 25", category=AircraftCategory.SAILPLANE)
    a2 = AircraftType(name="Concorde", category=AircraftCategory.PLANE)
    a3 = AircraftType(name="Untertasse", category=AircraftCategory.DRONE)

    db.session.add_all([a1, a2, a3])

    u1 = User(email="user1@email.de")
    u1.set_password("topsecret")

    Device(address="DD1234", device_type=DeviceType.FLARM, aircraft_type=a1, registration="D-1234", cn="34", user=u1)
    Device(address="DD4711", device_type=DeviceType.FLARM, aircraft_type=a2, registration="D-4711", cn="11", user=u1)

    u2 = User(email="user2@email.de")
    u2.set_password("evenmoresecret")

    Device(address="ABCDEF", device_type=DeviceType.OGN, aircraft_type=a3, registration="D-OTTO", cn="TO", user=u2)

    Receiver(name="Koenigsdf", antenna=Antenna.CHINESE_9DB_JPOLE, preamplifier=Preamplifier.TERRA_AB010, rx_filter=RxFilter.CAVITY, sdr_dongle=SdrDongle.RTLSDR_COM, user=u1)

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    build_db_from_ddb()
