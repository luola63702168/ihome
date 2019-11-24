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
    # 业务逻辑处理
    # 生成验证码图片
    # 名字，真实文本， 图片数据byte
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中
    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        #                   记录名字                          有效期                              记录值
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR,  errmsg="save image code id failed")
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码失败")

        # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
@api.route("/sms_codes/<re(r'1[3-9]\d{9}'):mobile>")
def get_sms_code(mobile):
    '''获取短信验证码'''
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 校验
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")  # 如果没有手机号就访问不到该视图，而且有正则的原因，手机号一定正确，所以无需校验手机号
    # 业务逻辑
    # 在redis中取出真实的验证码和用户填写的进行对比
    try:
        real_image_code = redis_store.get(f"image_code_{image_code_id}")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="redis数据库异常")
    # 判断real_image_code是否过期
    if real_image_code is None:
        # 标示没有或者过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 和用户的值进行对比
    if real_image_code.lower().decode() != image_code.lower():
        # print(real_image_code.lower().decode(),image_code.lower())
        # 填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于这个手机号是否在60s以内发送过验证码，如果有，认为操作频繁
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
        # print(send_flag)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后重试")

    # 判断手机号是否存在（先判断一下，在注册的时候还会判断，这里只是让用户可以提前知道自己的手机号注册过了，提高用户体验）
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:  # 说明查询没有异常
        if user is not None:
            # 表示手机号已存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    # 如果手机号不存在，则生成短信验证码(6位，不够补0)
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, "existence")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # celery异步发送短信
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    # celery异步发送短信，返回的是结果对象
    # result = send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    # 可以保存result这个对象，什么时候用得到再取即可
    # # 通过get方法获取celery异步执行结果(默认阻塞行为，可以设置超时时间，超过超时时间，就会立马返回)
    # ret = result.get()
    # print(ret)

    # 返回
    return jsonify(errno=RET.OK, errmsg="发送成功")



# # GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
# @api.route("/sms_codes/<re(r'1[3-9]\d{9}'):mobile>")
# def get_sms_code(mobile):
#     '''获取短信验证码'''
#     # 获取参数
#     image_code = request.args.get("image_code")
#     image_code_id = request.args.get("image_code_id")
#     # 校验
#     if not all([image_code,image_code_id]):
#         return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")  # 如果没有手机号就访问不到该视图，而且有正则的原因，手机号一定正确，所以无需校验手机号
#     # 业务逻辑
#     # 在redis中取出真实的验证码和用户填写的进行对比
#     try:
#         real_image_code = redis_store.get(f"image_code_{image_code_id}")
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR,errmsg="redis数据库异常")
#     # 判断real_image_code是否过期
#     if real_image_code is None:
#         # 标示没有或者过期
#         return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
#
#     # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
#     try:
#         redis_store.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     # 和用户的值进行对比
#     if real_image_code.lower().decode() != image_code.lower():
#         # print(real_image_code.lower().decode(),image_code.lower())
#         # 填写错误
#         return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
#
#     # 判断对于这个手机号是否在60s以内发送过验证码，如果有，认为操作频繁
#     try:
#         send_flag = redis_store.get("send_sms_code_%s" % mobile)
#         # print(send_flag)
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if send_flag is not None:
#             return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60秒后重试")
#
#     # 判断手机号是否存在（先判断一下，在注册的时候还会判断，这里只是让用户可以提前知道自己的手机号注册过了，提高用户体验）
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         current_app.logger.error(e)
#     else:  # 说明查询没有异常
#         if user is not None:
#             # 表示手机号已存在
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#     # 如果手机号不存在，则生成短信验证码(6位，不够补0)
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     # 保存真实验证码
#     try:
#         redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, "existence")
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
#
#     # 发送短信
#     try:
#         ccp = CCP()
#         result = ccp.sendTemplateSMS(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
#
#     # 返回值
#     if result == 0:
#         # 发送成功
#         return jsonify(errno=RET.OK, errmsg="发送成功")
#     else:
#         return jsonify(errno=RET.THIRDERR, errmsg="发送失败")
#
#






















