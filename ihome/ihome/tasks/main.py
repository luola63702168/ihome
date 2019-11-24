# coding: utf-8
# 以工程的方式管理celery

from celery import Celery

from ihome.tasks import config
# 定义celery对象
celery_app = Celery("ihome")

# 引入配置信息
celery_app.config_from_object(config)  # 也可以以字符串的形式传递配置文件所在目录

# 自动搜寻异步任务(任务文件必须tasks命名)
celery_app.autodiscover_tasks(["ihome.tasks.sms"])









