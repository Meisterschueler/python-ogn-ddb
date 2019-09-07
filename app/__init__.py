# flake8: noqa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_babel import Babel, _
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name="ddb admin", template_mode="bootstrap3")
login = LoginManager(app)
login.login_view = "login"
login.login_message_category = "danger"
login.localize_callback = _
bootstrap = Bootstrap(app)
mail = Mail(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    from flask import request

    return request.accept_languages.best_match(app.config["LANGUAGES"])


from app import routes, models, errors, legacy_routes, cli, admin_views

cli.register(app)
