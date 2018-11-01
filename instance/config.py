import os


class Config(object):
    '''Class to create default configurations'''
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    APP_SETTINGS = os.getenv("APP_SETTINGS")


class Development(Config):
    '''Class to set development mode configurations'''
    DEBUG = True


class Testing(Config):
    '''Class to set Testing mode configurations'''
    DB_NAME = os.getenv("TEST_DB_NAME")
    DB_HOST = os.getenv("TEST_DB_HOST")
    DB_USER = os.getenv("TEST_DB_USER")
    DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
    APP_SETTINGS = "testing"
    DEBUG = False

'''A dictionary to store all configurations for easy access'''
app_config = {
    "development": Development,
    "testing": Testing
}
