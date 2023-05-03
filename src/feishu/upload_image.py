# -*- coding: UTF-8 -*-
from feishu.feishu_conf import feishu_conf
from util.logger import app_logger

from larksuiteoapi.api import (
    Request,
    FormData,
    set_timeout,
    set_is_response_stream,
    set_response_stream,
)

from larksuiteoapi import ACCESS_TOKEN_TYPE_TENANT


def upload_image(img_data):
    formData = FormData()
    formData.add_param("image_type", "message")
    formData.add_param("image", img_data)
    req = Request("im/v1/images", "POST", ACCESS_TOKEN_TYPE_TENANT, formData)
    resp = req.do(feishu_conf)
    app_logger.debug("request id = %s" % resp.get_request_id())
    app_logger.debug(resp)
    if resp.code == 0:
        app_logger.debug(resp.data)
        return resp.data["image_key"]
    else:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)


def test_download_file(image_key, image_file, timeout=False):
    body = {
        "image_key": image_key,
    }
    operations = [set_is_response_stream()]
    if timeout:
        operations += [set_timeout(0.001)]

    f = open(image_file, "wb")
    operations += [set_response_stream(f)]

    req = Request(
        "image/v4/get", "GET", [ACCESS_TOKEN_TYPE_TENANT], body, request_opts=operations
    )
    resp = req.do(feishu_conf)
    app_logger.debug("request id = %s" % resp.get_request_id())
    app_logger.debug("http status code = %s" % resp.get_http_status_code())
    if resp.code != 0:
        app_logger.debug(resp.msg)
        app_logger.debug(resp.error)
