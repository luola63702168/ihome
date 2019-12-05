# coding: utf-8
import random

from flask import current_app,jsonify,make_response,request

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome import redis_store,constants,db
from ihome.models import User
from ihome.libs.yuntongxun.sms import CCP
# from ihome.tasks.task_sms import send_sms # 模块级celery
from ihome.tasks.sms.tasks import send_sms  # 工程级celery

# GET 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :params image_code_id: 图片验证码编号
    :return: 正常：返回的是验证码图片 异常：返回json
    """
    name, text, image_data = captcha.generate_captcha()
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码失败")
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[3-9]\d{9}'):mobile>")
def get_sms_code(mobile):
    '''获取短信验证码'''
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        real_image_code = redis_store.get(f"image_code_{image_code_id}")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="redis数据库异常")
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    if real_image_code.lower().decode() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后重试")
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    sms_code = "%06d" % random.randint(0, 999999)
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, "existence")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    return jsonify(errno=RET.OK, errmsg="发送成功")

























