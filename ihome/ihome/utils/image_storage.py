# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, put_data, etag  # 使用put_data 直接上传二进制数据
import qiniu.config

access_key = '6plepVXwHlfkkPQnZKVXBnDGrgFlIHACse41X2-8'
secret_key = 'jm4o9bUZELdWIOg2DtGMrdhaDnZ9yU799bK04aav'


def storage(filedata):
    '''
    上传文件到七牛
    :param filedata:要上传的二进制文件
    :return:
    '''
    q = Auth(access_key, secret_key)
    bucket_name = 'rusiihome'
    token = q.upload_token(bucket_name, None, 3600)
    ret, info = put_data(token, None, filedata)
    if info.status_code == 200:
        return ret.get("key")
    else:
        raise Exception("上传七牛失败")


if __name__ == '__main__':
    with open("../static/images/home01.jpg", "rb") as f:
        file_data = f.read()
        storage(file_data)
