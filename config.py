import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///" + os.path.join(basedir, "data.sqlite"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ["en", "de"]
    
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # administrator list
    ADMINS = ['your-gmail-username@gmail.com']
    
    @staticmethod
    def init_app(app):
        pass

config = {
    'development': Config,
    'testing': Config,
    'production': Config,
              
    'default': Config
}