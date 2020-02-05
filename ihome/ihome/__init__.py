# coding: utf-8
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect

from config import config_map
from ihome.utils.commons import ReConverter

# 数据库连接的两种方式
# 1
# db = SQLAlchemy(app)
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None

# 配置日志信息
logging.basicConfig(level=logging.INFO)
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    创建flask应用对象
    :param config_name: str 配置模式（"develop","product"）
    :return: 返回开发环境的app或者生产环境的app
    """
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 2 使用app初始化db
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, db=config_class.DB)

    # 利用flask-session，将session保存到redis中
    Session(app)
    # 为flask补充csrf防护(利用了钩子@app.before_request)
    CSRFProtect(app)

    # 为flask添加自定义的转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    # 注册提供静态文件的蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)
    return app
