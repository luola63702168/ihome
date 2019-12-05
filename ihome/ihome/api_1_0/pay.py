# coding: utf-8
import os

from flask import g, current_app, jsonify, request
from alipay import AliPay

from ihome.models import Order
from ihome.utils.response_code import RET
from . import api
from ihome.utils.commons import login_required
from ihome import constants, db


@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    """
    支付宝支付
    :return:
    """
    user_id = g.user_id
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id,
                                   Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="订单数据有误")
    alipay_client = AliPay(
        appid="2016101300676042",
        app_notify_url=None,
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )
    order_string = alipay_client.api_alipay_trade_wap_pay(
        out_trade_no=order.id,
        total_amount=str(order.amount / 100.0),
        subject="爱家租房 %s" % order.id,
        return_url="http://127.0.0.1:5000/payComplete.html",
        notify_url=None
    )
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})


@api.route("/order/payment", methods=["PUT"])
@login_required
def save_order_payment_result():
    """保存订单支付结果"""
    alipay_dict = request.form.to_dict()
    alipay_sign = alipay_dict.pop("sign")
    alipay_client = AliPay(
        appid="2016101300676042",
        app_notify_url=None,
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )
    result = alipay_client.verify(alipay_dict, alipay_sign)
    if result:
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")
        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
    return jsonify(errno=RET.OK, errmsg="OK")
