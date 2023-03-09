# _author: Coke
# _date: 2022/12/30 22:09
import logging

from application.api import api
from application import utils, OSS_DICT
from flask import request
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


def tencent_upload(file, save_name):
    config = CosConfig(
        Region=OSS_DICT.get('Region'),
        SecretId=OSS_DICT.get('SecretId'),
        SecretKey=OSS_DICT.get('SecretKey')
    )
    client = CosS3Client(config)

    client.put_object(
        Bucket=OSS_DICT.get('Bucket'),
        Body=file,
        Key=save_name
    )
    url = client.get_object_url(
        Bucket=OSS_DICT.get('Bucket'),
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

    try:
        url = tencent_upload(file, file.filename)
        return utils.rander(utils.OK, data=dict(url=url))
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATA_ERR, '上传文件失败')
