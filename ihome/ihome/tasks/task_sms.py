# coding: utf-8
# 此处为模块级celery（项目暂时未应用此模块）

from celery import Celery

from ihome.libs.yuntongxun.sms import CCP

# 定义celery对象

celery_app = Celery("ihome",broker='redis://127.0.0.1:6379/6')


# 不是tasks
@celery_app.task
def send_sms(to, datas, tempId):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.sendTemplateSMS(to,datas,tempId)







