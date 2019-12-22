import redis


# coding: utf-8
class Config(object):
    '''配置信息'''

    SECRET_KEY = "sdasdwasA*SADHio12344**"
    # mysql
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    DB = 7  

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=7)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    '''开发模式配置信息'''
    DEBUG = True


class ProductionConfig(object):
    '''生产环境配置信息'''
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
