# _author: Coke
# _date: 2022/12/30 22:09

from application.api import api
from application import utils
from flask import request
from logs.tencent import *
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

import logging
import time


def tencent_upload(file, save_name):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    client.put_object(
        Bucket=bucket,
        Body=file,
        Key=save_name
    )
    url = client.get_object_url(
        Bucket=bucket,
        Key=save_name
    )
    return url


@api.route('/upload/file/image', methods=['POST', 'PUT'])
# @utils.login_required
# @utils.permissions_required
def upload_file_image():
    """ 上传文件到腾讯云服务器 """

    file = request.files.get('file')

    if not file:
        return utils.rander(utils.BODY_ERR)

    url = tencent_upload(file, file.filename)
    return utils.rander(utils.OK, data=dict(url=url))
