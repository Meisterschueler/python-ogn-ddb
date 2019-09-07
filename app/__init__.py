# flake8: noqa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_babel import Babel, _
from config import config

db = SQLAlchemy()
admin = Admin(name="ddb admin", template_mode="bootstrap3")
login = LoginManager()
login.login_view = "login"
login.login_message_category = "danger"
login.localize_callback = _
bootstrap = Bootstrap()
mail = Mail()
babel = Babel()

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    migrate = Migrate(app, db)

    db.init_app(app)
    admin.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    # from app import routes, models, errors, legacy_routes, admin_views
    from app.main import bp as blueprint_main

    app.register_blueprint(blueprint_main)

    return app


@babel.localeselector
def get_locale():
    from flask import request

    return request.accept_languages.best_match(app.config["LANGUAGES"])

