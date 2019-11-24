# coding: utf-8
import re

from flask import request,jsonify,current_app,session
from sqlalchemy.exc import IntegrityError  # 出现字段不允许出现重复时的异常

from . import api
from ihome.utils.response_code import RET
from ihome import redis_store,db,constants
from ihome.models import User
from werkzeug.security import generate_password_hash,check_password_hash  # 生成加密密码和检验密码


@api.route("/users", methods=["POST"])
def register():
    '''注册
    请求的参数： 手机号、短信验证码、密码、确认密码
    参数格式：json
    '''
    # 获取

    req_dict = request.get_json()
    mobile=req_dict.get("mobile")
    sms_code=req_dict.get("sms_code")
    password=req_dict.get("password")
    password2=req_dict.get("password2")
    # print(mobile,sms_code,password,password2)
    # 校验
    if not all([mobile,sms_code,password,password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断手机号格式
    if not re.match(r'1[3-9]\d{9}',mobile):
        # if条件满足的时候，正则不满足，所以返回None 所以格式不匹配
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")
    # 两次密码校验（本身还要进行限制检测）
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    # 从redis中取出验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户填写的验证码的正确性
    if real_sms_code.decode() != sms_code:
        # print(type(real_sms_code.decode()),type(sms_code))
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误,请重新获取验证码")

    # 判断用户手机号是否注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     # 比起获取手机验证码阶段，这时候就不允许数据库查询出现问题了，如果出现就不再往下走了
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # else:
    #     if user is not None:
    #         # 表示手机号已存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    # 保存用户资料(利用手机号的唯一约束)

    # 盐值加密
    user = User(name=mobile, mobile=mobile)
    # user.generate_password_hash(password)
    user.password = password  # 利用property实现给用户设置密码的逻辑
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 保存登录状态到session中(已经通过flask-session改变了session存储机制，所以直接用最开始的存储方法即可)
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    # 返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/sessions",methods=["POST"])
def login():
    '''
    登录
    参数：手机号、密码、json
    :return:
    '''
    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    # 校验参数
    if not all([mobile,password]):
        return jsonify(erron=RET.PARAMERR,errmsg="参数不完整")
    if not re.match(r"1[3-9]\d{9}",mobile):
        return jsonify(erron=RET.PARAMERR,errmsg="手机号格式错误")
    # 防止暴力测试（判断错误次数是否超过限制）
    # redis记录："access_nums_ip":"次数"
    user_ip = request.remote_addr
    # print(user_ip)
    try:
        access_nums=redis_store.get(f"access_num_{user_ip}")
        if access_nums is not None:
            access_nums=access_nums.decode()
        # print(access_nums,"*"*100)
    except Exception as e:
        current_app.logger.error(e)  # redis查不出来就算了，可以继续进行，但是要记录错误，利于及时处理
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR,errmsg="错误次数过多，请稍候重试")
    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    # 用户和密码的校验放置一起（不要返回用户不存在，返回的只有用户名或密码不存在，避免别人可以通过于此获取哪些手机号是我们的用户）
    if user is None or not user.check_passed(password):
        # 验证失败,返回提示信息，记录错误错误次数
        try:
            # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为0,当然，你也可以设置步长，如果不设置，默认为1
            redis_store.incr("access_num_%s" % user_ip)
            # 虽说每一次都要设置一次有效期，是不合理的，但是如果在设置有效期的时候进行一次查询并判断次数，是更不合理的，所以就设置五次有效期，虽说最后一次设置才是真正有用的
            redis_store.expire("access_num_%s" % user_ip,constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    # 验证成功，保存登录状态，session
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="登录成功")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token  # 避免csrf丢失问题
    return jsonify(errno=RET.OK, errmsg="OK")































