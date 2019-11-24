# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
from .CCPRestSDK import REST
# from CCPRestSDK import REST

# 主帐号
accountSid = '8aaf07086e0115bb016e55523e4f2dfc'

# 主帐号Token
accountToken = '611bc08e31504fd5853806d44833b67b'

# 应用Id
appId = '8a216da86e011fa3016e5558efaf2d24'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):
    '''用于自己封装的发送短信的辅助类'''
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            obj = super().__new__(cls)  # obj本身就是这个对象
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    # sendTemplateSMS(手机号码,内容数据,模板Id)
    def sendTemplateSMS(self,to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        # for k, v in result.items():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.items():
        #             print('%s:%s' % (k, s))
        #     else:
        #         print('%s:%s' % (k, v))
        # statusCode: 000000
        # smsMessageSid: 0
        # ccb748d32f74cea93391f071ef4c8e9
        # dateCreated: 20191110232443
        status_code=result.get("statusCode")
        if status_code == "000000":  # 表示发送成功
            return 0
        else:
            return -1

if __name__ == '__main__':
    ccp = CCP()
    ret = ccp.sendTemplateSMS("13676977767",["1234","5"],1)
    print(ret)


