# _author: Coke
# _date: 2022/12/30 22:09

from application.api import api
from application import utils, OSS_DICT
from flask import request
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

import logging
import re


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


def match_image_extension(filename):
    image_extensions = r'\.(jpg|jpeg|png|gif|bmp)$'
    pattern = re.compile(image_extensions, re.IGNORECASE)
    return re.search(pattern, filename) is not None


@api.route('/upload/file/image', methods=['POST', 'PUT'])
# @utils.login_required
# @utils.permissions_required
def upload_file_image():
    """ 上传文件到腾讯云服务器 """

    file = request.files.get('file')

    if not file:
        return utils.rander(utils.BODY_ERR)

    if not match_image_extension(file.filename):
        return utils.rander(utils.DATA_ERR, msg='上传图片只能是 JPG 、PNG、GIF、BMP 格式')

    try:
        url = tencent_upload(file, file.filename)
        return utils.rander(utils.OK, data=dict(url=url))
    except Exception as e:
        logging.error(e)
        return utils.rander(utils.DATA_ERR, '上传文件失败')
