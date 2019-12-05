from celery import Celery

from ihome.libs.yuntongxun.sms import CCP

celery_app = Celery("ihome", broker='redis://127.0.0.1:6379/6')


@celery_app.task
def send_sms(to, datas, tempId):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.sendTemplateSMS(to, datas, tempId)
