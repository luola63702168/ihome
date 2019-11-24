# coding: utf-8
import logging
from logging.handlers import RotatingFileHandler # 文件路径 文件大小 文件数量

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # mysql
import redis
from flask_session import Session  # 改变session存储
from flask_wtf import CSRFProtect  # csrf防护

from config import config_map  # 配置信息映射
from ihome.utils.commons import ReConverter
# 数据库连接的两种方式
# 1
# db = SQLAlchemy(app)
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None

# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.INFO)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)





# 工厂模式（根据不同配置信息，确定线上还是线下环境)
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
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,db=config_class.DB)  # 因为和生产模式有关，所以要放置这里，也就需要利用global修改全局变量了

    # 利用flask-session，将session保存到redis中
    Session(app)  # 这个对象不去设置session，只是修改了flask的默认session机制，并且还可以自动读取与之相关的配置信息。
    # 为flask补充csrf防护(利用了钩子@app.before_request)，和session一样，并不会直接的去使用它,仅做校验工作
    CSRFProtect(app)

    # 为flask添加自定义的转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    # from . import api_1_0  这样导入也是可以的
    from ihome import api_1_0  # 延迟导入解决循环引用
    app.register_blueprint(api_1_0.api,url_prefix="/api/v1.0")

    # 注册提供静态文件的蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)
    return app

