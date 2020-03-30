# flake8: noqa
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_babel import Babel, _
from config import config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name="ddb admin", template_mode="bootstrap3")
login = LoginManager()
login.login_view = "main.login"
login.login_message_category = "danger"
login.localize_callback = _
bootstrap = Bootstrap()
mail = Mail()
babel = Babel()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    # from app import routes, models, errors, legacy_routes, admin_views
    from app.main import bp as blueprint_main

    app.register_blueprint(blueprint_main)

    from flask_admin.contrib.sqla import ModelView
    from app.models import AircraftType, Device, DeviceClaim, Receiver, User

    admin.add_view(ModelView(AircraftType, db.session))
    admin.add_view(ModelView(Device, db.session))
    admin.add_view(ModelView(DeviceClaim, db.session))
    admin.add_view(ModelView(Receiver, db.session))
    admin.add_view(ModelView(User, db.session))

    return app


@babel.localeselector
def get_locale():
    from flask import request

    return request.accept_languages.best_match(current_app.config["LANGUAGES"])
