from config.app.base import BASE_DIR
import environ

env = environ.Env()
DB_DEVELOP_NAME = env.str("DB_NAME", "")
DB_DEVELOP_USER = env.str("DB_USER", "")
DB_DEVELOP_PASSWORD = env.str("DB_PASSWORD", "")
DB_DEVELOP_HOST = env.str("DB_HOST", "")
DB_DEVELOP_PORT = env.str("DB_PORT", "")

DATABASE_CONFIG = {
    'local': {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'mysql': {
            "ENGINE": "django.db.backends.mysql",
            "NAME": DB_DEVELOP_NAME,
            "USER": DB_DEVELOP_USER,
            "PASSWORD": DB_DEVELOP_PASSWORD,
            "HOST": DB_DEVELOP_HOST,
            "PORT": DB_DEVELOP_PORT,
        },
    },
    'prod': {
        'mysql': {
            "ENGINE": "django.db.backends.mysql",
            "NAME": DB_DEVELOP_NAME,
            "USER": DB_DEVELOP_USER,
            "PASSWORD": DB_DEVELOP_PASSWORD,
            "HOST": DB_DEVELOP_HOST,
            "PORT": DB_DEVELOP_PORT,
        }
    }
}
