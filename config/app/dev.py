from config.app.base import *
from config.db.database import DATABASE_CONFIG

DEBUG = True

ALLOWED_HOSTS = ["*"]

THIRDS_APPS += []

INSTALLED_APPS = COMMON_APPS + THIRDS_APPS + MY_APPS 

MIDDLEWARE += []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE = env.str("DATABASE", "sqlite")

DATABASES = {'default': DATABASE_CONFIG["local"][DATABASE]}
