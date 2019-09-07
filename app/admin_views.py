from flask_admin.contrib.sqla import ModelView
from app import db, admin
from app.models import AircraftType, DeviceClaim

admin.add_view(ModelView(AircraftType, db.session))
admin.add_view(ModelView(DeviceClaim, db.session))
