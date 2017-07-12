# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os
from dotenv import load_dotenv


class BaseConfig(object):
    """Define base configuration for the GRASS-rest API"""
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
    SECRET_KEY = os.environ.get('GREST_SECRET_KEY',
                                'this-really-needs-to-be-changed')
    # POSTGRESQL
    # DB_USER = 'user'
    # DB_PASSWORD = 'password'
    # DB_NAME = 'restplusdb'
    # DB_HOST = 'localhost'
    # DB_PORT = 5432
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     name=DB_NAME,
    # )

    # SQLITE
    SQLALCHEMY_DATABASE_URI = os.environ.get('GREST_SQLALCHEMY_DATABASE_URI',
            'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "grass-rest.db")))
    DEBUG = os.environ.get('GREST_DEBUG', False)

    AUTHORIZATIONS = {
        'oauth2_password': {
            'type': 'oauth2',
            'flow': 'password',
            'scopes': {},
            'tokenUrl': '/auth/oauth2/token',
        },
        # TODO: implement other grant types for third-party apps
        #'oauth2_implicit': {
        #    'type': 'oauth2',
        #    'flow': 'implicit',
        #    'scopes': {},
        #    'authorizationUrl': '/auth/oauth2/authorize',
        #},
    }

    ENABLED_MODULES = (os.environ.get('GREST_ENABLED_MODULES').split()
                       if 'GREST_ENABLED_MODULES' in os.environ else
                       (
                            'auth',

                            'users',
                            'teams',

                            'api',
                        ))

    STATIC_ROOT = os.environ.get('GREST_STATIC_ROOT',
                                 os.path.join(PROJECT_ROOT, 'static'))

    SWAGGER_UI_JSONEDITOR = os.environ.get('GREST_SWAGGER_UI_JSONEDITOR',
                                           True)
    SWAGGER_UI_OAUTH_CLIENT_ID = os.environ.get('GREST_SWAGGER_UI_OAUTH_CLIENT_ID',
                                                'documentation')
    SWAGGER_UI_OAUTH_REALM = os.environ.get('GREST_SWAGGER_UI_OAUTH_REALM',
                                            "Authentication for GRASS-rest server documentation")
    SWAGGER_UI_OAUTH_APP_NAME = os.environ.get('GREST_SWAGGER_UI_OAUTH_APP_NAME',
                                               "GRASS-rest server documentation")

    # TODO: consider if these are relevant for this project
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('GREST_SERVER_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('CLOUDSML_API_SERVER_SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
