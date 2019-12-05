# coding: utf-8
import re

from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError

from . import api
from ihome.utils.response_code import RET
from ihome import redis_store, db, constants
from ihome.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@api.route("/users", methods=["POST"])
def register():
    '''注册
    请求的参数： 手机号、短信验证码、密码、确认密码
    参数格式：json
    '''
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if not re.match(r'1[3-9]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    if real_sms_code.decode() != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误,请重新获取验证码")
    # 盐值加密
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(password)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/sessions", methods=["POST"])
def login():
    '''
    登录
    参数：手机号、密码、json
    :return:
    '''
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    if not all([mobile, password]):
        return jsonify(erron=RET.PARAMERR, errmsg="参数不完整")
    if not re.match(r"1[3-9]\d{9}", mobile):
        return jsonify(erron=RET.PARAMERR, errmsg="手机号格式错误")
    user_ip = request.remote_addr
    try:
        access_nums = redis_store.get(f"access_num_{user_ip}")
        if access_nums is not None:
            access_nums = access_nums.decode()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍候重试")
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    if user is None or not user.check_passed(password):
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    name = session.get("name")
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="OK")
