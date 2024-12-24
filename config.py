class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/IESCP_V2.sqlite3'
    SECURITY_JOIN_USER_ROLES = True
    SECRET_KEY = "secretkey"
    SECURITY_PASSWORD_SALT = "salt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 15
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_DB = 0