import os


class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class Development(Config):
    DEBUG = True


class Testing(Config):
    DEBUG = False


app_config = {
    "development": Development,
    "testing": Testing
}
