# coding: utf-8
from flask import Blueprint

# 创建蓝图对象

api = Blueprint("api_1_0", __name__)

# demo中使用了api 所以要放置其下方（避免循环引用）
# 导入蓝图的视图
from . import verify_code,passport,profile,houses,orders,pay
