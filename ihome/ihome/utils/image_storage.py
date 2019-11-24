# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file,put_data, etag  # 使用put_data 直接上传二进制数据即可
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = '6plepVXwHlfkkPQnZKVXBnDGrgFlIHACse41X2-8'
secret_key = 'jm4o9bUZELdWIOg2DtGMrdhaDnZ9yU799bK04aav'


def storage(filedata):
    '''
    上传文件到七牛
    :param filedata:要上传的二进制文件
    :return:
    '''
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'rusiihome'

    # # 上传后保存的文件名（屏蔽掉 让其自动帮我们生成）
    # key = 'my-python-logo.png'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, None, filedata)
    if info.status_code==200:
        return ret.get("key")
    else:
        # 上传失败
        raise Exception("上传七牛失败")
    # print(info)
    # print("*"*100)
    # print(ret)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)


if __name__ == '__main__':
    with open("../static/images/home01.jpg","rb") as f:
        file_data = f.read()
        storage(file_data)