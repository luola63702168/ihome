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
    DB = 7  # 存储验证码记录,session

    # flask-session配置
    SESSION_TYPE = "redis"  # 使用什么去存
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,db=7)  # redis实例对象
    SESSION_USE_SIGNER = True  # 对cookie中的session id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位s


class DevelopmentConfig(Config):
    '''开发模式配置信息'''
    DEBUG = True  # 开启debug的时候会强制覆盖掉log日志级别


class ProductionConfig(object):
    '''生产环境配置信息'''
    pass


config_map = {
    "develop":DevelopmentConfig,
    "product":ProductionConfig
}
