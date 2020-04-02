import os
import csv
from app import db
from app.models import Antenna, AircraftType, AircraftCategory, User, Device, DeviceType, Preamplifier, Receiver, RxFilter, SdrDongle


basepath = os.path.dirname(os.path.realpath(__file__))


def import_devices():
    # We don't have the 'original' ddb with emails so we create a single user who takes it all
    user = User(email="user1@email.de")
    user.set_password("topsecret")
    db.session.add(user)

    with open(os.path.join(basepath, "ressources/ddb.txt")) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for row in csvreader:
            device_type = {"F": DeviceType.FLARM, "I": DeviceType.ICAO, "O": DeviceType.OGN}[row["#DEVICE_TYPE"]]
            address = row["DEVICE_ID"]
            aircraft_type_name = row["AIRCRAFT_MODEL"]
            registration = row["REGISTRATION"]
            cn = row["CN"]
            show_track = row["TRACKED"] == "Y"
            show_identity = row["IDENTIFIED"] == "Y"
            aircraft_category = AircraftCategory.coerce(row["AIRCRAFT_TYPE"])

            aircraft_type = AircraftType.query.filter_by(name=aircraft_type_name).one_or_none()
            if not aircraft_type:
                aircraft_type = AircraftType(name=aircraft_type_name, category=aircraft_category)

            Device(device_type=device_type, aircraft_type=aircraft_type, address=address, registration=registration, cn=cn, show_track=show_track, show_identity=show_identity, user=user)

    db.session.commit()


def import_aircrafts():
    AircraftType.query.delete()
    with open(os.path.join(basepath, "ressources/aircrafts.csv")) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        for row in csvreader:
            id = row["ID"]
            category = AircraftCategory.coerce(row["CATEGORY"])
            model = row["MODEL"]

            aircraft_type = AircraftType(id=id, name=model, category=category)
            db.session.add(aircraft_type)

    db.session.commit()


def import_fakedata():
    a1 = AircraftType(name="ASK-13", category=AircraftCategory.SAILPLANE)
    a2 = AircraftType(name="ASH-25", category=AircraftCategory.SAILPLANE)
    a3 = AircraftType(name="Rhönlärche Ил-32", category=AircraftCategory.SAILPLANE)
    a4 = AircraftType(name="Aquila A210", category=AircraftCategory.PLANE)
    a5 = AircraftType(name="Concorde", category=AircraftCategory.PLANE)
    a6 = AircraftType(name="Eurofox", category=AircraftCategory.ULTRALIGHT)
    a7 = AircraftType(name="Gyrocopter", category=AircraftCategory.ULTRALIGHT)
    a8 = AircraftType(name="EC 120", category=AircraftCategory.HELICOPTER)
    a9 = AircraftType(name="EC 130", category=AircraftCategory.HELICOPTER)
    a10 = AircraftType(name="EC 135", category=AircraftCategory.HELICOPTER)
    a11 = AircraftType(name="DJI S800", category=AircraftCategory.DRONE)
    a12 = AircraftType(name="DJI S900", category=AircraftCategory.DRONE)
    a13 = AircraftType(name="DJI S1000", category=AircraftCategory.DRONE)
    a14 = AircraftType(name="Balloon", category=AircraftCategory.OTHER)
    a15 = AircraftType(name="Paraglider", category=AircraftCategory.OTHER)
    a16 = AircraftType(name="UFO", category=AircraftCategory.OTHER)

    db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16])

    u1 = User(email="user1@localhost")
    u1.set_password("topsecret1")

    Device(address="DD1234", device_type=DeviceType.FLARM, aircraft_type=a1, registration="D-1234", cn="34", user=u1)
    Device(address="DD4711", device_type=DeviceType.FLARM, aircraft_type=a2, registration="D-4711", cn="11", user=u1)

    u2 = User(email="user2@localhost")
    u2.set_password("topsecret2")

    Device(address="ABCDEF", device_type=DeviceType.OGN, aircraft_type=a3, registration="D-OTTO", cn="TO", user=u2)

    Receiver(name="Koenigsdf", antenna=Antenna.CHINESE_9DB_JPOLE, preamplifier=Preamplifier.TERRA_AB010, rx_filter=RxFilter.CAVITY, sdr_dongle=SdrDongle.RTLSDR_COM, user=u1)
    Receiver(name="Wank", antenna=Antenna.CHINESE_9DB_JPOLE, preamplifier=Preamplifier.NONE, rx_filter=RxFilter.CBP840, sdr_dongle=SdrDongle.RTLSDR_COM, user=u1)
    Receiver(name="Arber", antenna=Antenna.WIMO_SPERRTOPF, preamplifier=Preamplifier.NONE, rx_filter=RxFilter.CAVITY, sdr_dongle=SdrDongle.RTLSDR_COM, user=u1)
    Receiver(name="Marmolada", antenna=Antenna.CHINESE_9DB_JPOLE, preamplifier=Preamplifier.SELF_BUILT_WITH_FILTER, rx_filter=RxFilter.NONE, sdr_dongle=SdrDongle.RTLSDR_COM, user=u1)

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
