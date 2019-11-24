# coding: utf-8
import functools

from werkzeug.routing import BaseConverter
from flask import session,jsonify,g

from ihome.utils.response_code import RET


# 定义正则转换器
class ReConverter(BaseConverter):
    '''re转换器'''
    def __init__(self,url_map,regex):
        # 调用父类初始化方法
        super().__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 定义登录装饰器
def login_required(view_func):
    @functools.wraps(view_func)  # 把被装饰的函数的一些属性恢复（__name__等），这样就避免了改变被装饰函数的相关属性。
    def wrapper(*args,**kwargs):
        # 判断用户的登录状态
        user_id = session.get("user_id")
        # 如果用户登录的，执行视图函数
        if user_id is not None:
            g.user_id = user_id  # 只要在本次请求过程的函数都以通过g对象拿取user_id了（这里是装饰器函数和视图函数间的使用，假设有重定向的话，那么g对象就没有用了）
            return view_func(*args,**kwargs)
        else:
            # 如果未登录，返回json数据，告知未登录
            return jsonify(errno=RET.SESSIONERR,errmsg="用户未登录")
    return wrapper
























