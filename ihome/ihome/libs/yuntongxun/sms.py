# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
from .CCPRestSDK import REST
# from CCPRestSDK import REST

# ���ʺ�
accountSid = '8aaf07086e0115bb016e55523e4f2dfc'

# ���ʺ�Token
accountToken = '611bc08e31504fd5853806d44833b67b'

# Ӧ��Id
appId = '8a216da86e011fa3016e5558efaf2d24'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

class CCP(object):
    '''�����Լ���װ�ķ��Ͷ��ŵĸ�����'''
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            obj = super().__new__(cls)  # obj��������������
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance

    # sendTemplateSMS(�ֻ�����,��������,ģ��Id)
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
        if status_code == "000000":  # ��ʾ���ͳɹ�
            return 0
        else:
            return -1

if __name__ == '__main__':
    ccp = CCP()
    ret = ccp.sendTemplateSMS("13676977767",["1234","5"],1)
    print(ret)


