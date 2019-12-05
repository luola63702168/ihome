from ihome.libs.yuntongxun.sms import CCP
from ihome.tasks.main import celery_app


@celery_app.task
def send_sms(to, datas, tempId):
    """发送短信的异步任务"""
    ccp = CCP()
    ret = ccp.sendTemplateSMS(to, datas, tempId)
    return ret
