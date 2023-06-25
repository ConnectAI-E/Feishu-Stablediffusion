# -*- coding: UTF-8 -*-
from feishu.feishu_conf import feishu_conf
from util.logger import app_logger
import hashlib
from larksuiteoapi.service.image.v4 import Service as ImageV4Service
from larksuiteoapi.service.im.v1 import Service as ImV1Service
import io
from PIL import Image

from larksuiteoapi.api import (
    Request,
    FormData,
    set_timeout,
    set_is_response_stream,
    set_response_stream,
)

from larksuiteoapi import ACCESS_TOKEN_TYPE_TENANT

img_service = ImageV4Service(feishu_conf)
im_service = ImV1Service(feishu_conf)


def upload_image(img_data: Image):
    buffered = io.BytesIO()
    img_data.save(buffered, format="PNG")
    formData = FormData()
    formData.add_param('image_type', 'message')
    formData.add_param('image', buffered.getvalue())
    req = Request('im/v1/images', 'POST', ACCESS_TOKEN_TYPE_TENANT, formData)
    resp = req.do(feishu_conf)
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data['image_key']
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return None


def get_image(img_key):
    resp = img_service.images.get().set_image_key(img_key).do()
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return None


def get_message_resource(message_id, res_key, res_type='image'):
    resp = im_service.message_resources.get().set_message_id(message_id).set_file_key(res_key).set_type(res_type).do()
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return None


def download_image(image_key, image_file, timeout=False):
    body = {
        'image_key': image_key,
    }
    operations = [set_is_response_stream()]
    if timeout:
        operations += [set_timeout(0.001)]

    f = open(image_file, 'wb')
    operations += [set_response_stream(f)]

    req = Request('image/v4/get', 'GET', [ACCESS_TOKEN_TYPE_TENANT], body, request_opts=operations)
    resp = req.do(feishu_conf)
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug('http status code = %s' % resp.get_http_status_code())
    if resp.code != 0:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return resp.code == 0


def upload_file(file_name, file_type, file_data):
    '''
    :param file_name 带后缀的文件名
    :param file_type
        opus：上传opus音频文件其他格式的音频文件，请转为opus格式后上传，转换方式可参考：ffmpeg -i SourceFile.mp3 -acodec libopus -ac 1 -ar 16000 TargetFile.opus
        mp4：上传mp4视频文件
        pdf：上传pdf格式文件
        doc：上传doc格式文件
        xls：上传xls格式文件
    :param file_data 文件二进制数据
    '''
    formData = FormData()
    formData.add_param('file_name', file_name)
    formData.add_param('file_type', file_type)
    formData.add_param('file', file_data)
    req = Request('im/v1/files', 'POST', ACCESS_TOKEN_TYPE_TENANT, formData)
    resp = req.do(feishu_conf)
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data['file_key']
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return None


def get_file(file_key):
    body = {
        'file_key': file_key,
    }
    req = Request('im/v1/files', 'GET', ACCESS_TOKEN_TYPE_TENANT, body)
    resp = req.do(feishu_conf)
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return None


def download_file(file_key, file_name, timeout=False):
    body = {
        'file_key': file_key,
    }
    operations = [set_is_response_stream()]
    if timeout:
        operations += [set_timeout(0.001)]

    f = open(file_name, 'wb')
    operations += [set_response_stream(f)]

    req = Request('im/v1/files', 'GET', ACCESS_TOKEN_TYPE_TENANT, body, request_opts=operations)
    resp = req.do(feishu_conf)
    app_logger.debug('request id = %s' % resp.get_request_id())
    app_logger.debug('http status code = %s' % resp.get_http_status_code())
    if resp.code != 0:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)

    return resp.code == 0


def get_md5(file):
    hash_md5 = hashlib.md5()
    chunk_size = 8192
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def compare_file(file1, file2):
    md5_file1 = get_md5(file1)
    md5_file2 = get_md5(file2)

    return md5_file1 == md5_file2
