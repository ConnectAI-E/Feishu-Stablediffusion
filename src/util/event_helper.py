import json
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from util.logger import app_logger
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi.api import (
    Request,
    FormData,
    set_timeout,
    set_is_response_stream,
    set_response_stream,
)
from larksuiteoapi import ACCESS_TOKEN_TYPE_TENANT



# bot need to be mentioned in first place
def is_mention_bot(event: MessageReceiveEvent) -> bool:
    mentions = event.event.message.mentions
    if event.event.message.mentions is None or mentions[0].name != app_config.BOT_NAME:
        return False

    return True

def get_mention_message(event: MessageReceiveEvent) -> str:
    if is_mention_bot(event):
        content = json.loads(event.event.message.content)
        if "text" in content:
            text = content["text"]
            return text.split(" ", 1)[1]
        
    return None

def get_image_source(img_key, message_id):
    body = {
        "image_key": img_key,
        "message_id": message_id
    }
    req = Request("/open-apis/im/v1/messages/" + message_id +'/resources/'+img_key + '?type=image', "GET", [ACCESS_TOKEN_TYPE_TENANT], body)
    resp = req.do(feishu_conf)
    if resp.code == 0:
        return resp.data
    else:
        app_logger.debug(resp.msg)

def get_pure_message(event: MessageReceiveEvent) -> str:

    if event.event.message.message_type == "image":
        content = event.event.message.content
        content_dict = json.loads(content)  # 将字符串解析成字典对象
        image_key = content_dict["image_key"]  # 获取字典中 image_key 的值
        message_id = event.event.message.message_id
        return get_image_source(image_key, message_id)

    if event.event.message.chat_type == "group":
        return get_mention_message(event)
    else:
        return json.loads(event.event.message.content)['text']