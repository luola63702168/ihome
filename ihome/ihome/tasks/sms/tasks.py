# coding: utf-8
# 定义的模块名字是固定的，这样在执行任务的时候celery会自动的寻找tasks文件


from ihome.libs.yuntongxun.sms import CCP
from ihome.tasks.main import celery_app

# 不是tasks
@celery_app.task
def send_sms(to, datas, tempId):
    """发送短信的异步任务"""
    ccp = CCP()
    # ccp.sendTemplateSMS(to,datas,tempId)
    ret = ccp.sendTemplateSMS(to,datas,tempId)
    return ret
















