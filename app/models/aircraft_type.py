from app import db
from .aircraft_category import AircraftCategory


class AircraftType(db.Model):
    __tablename__ = "aircraft_types"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(32), nullable=False)
    category = db.Column(db.Enum(AircraftCategory), nullable=False)

    @classmethod
    def choices(cls):
        return [(item.id, item.name) for item in cls.query.order_by(cls.category | cls.name)]

    # def __repr__(self):
    #    return "AircraftType(name={self.name}, category={self.category})".format(self=self)
