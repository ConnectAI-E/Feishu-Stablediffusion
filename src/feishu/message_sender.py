import json
import time
import attr
from larksuiteoapi.api import Request, set_timeout
from larksuiteoapi.service.im.v1 import Service as ImService, model
from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_FEISHU
from util.app_config import app_config
from feishu.feishu_conf import feishu_conf
from util.logger import app_logger

@attr.s
class Message(object):
    message_id = attr.ib(type=str)  # type: ignore


class MessageSender:
    def __init__(self, conf: Config):
        if not conf:
            raise Exception("conf is required")
        self.conf = conf

    def send_text_message(self, chat_id, user_id, msg_id, msg):
        body = {
            "chat_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": f'<at user_id="{user_id}"></at> {msg}'}),
        }
        req = Request(
            f"/open-apis/im/v1/messages/{msg_id}/reply",
            "POST",
            ACCESS_TOKEN_TYPE_TENANT,
            body,
            output_class=Message,
            request_opts=[set_timeout(3)],
        )
        resp = req.do(self.conf)
        app_logger.debug("send_text_message:%s", msg)
        if resp.code == 0:
            # store the message in the chat history
            return True
        else:
            app_logger.error(
                "send message failed, code:%s, msg:%s, error:%s",
                resp.code,
                resp.msg,
                resp.error,
            )
            return False

    # 发送消息卡片
    def send_message_card(self, chat_id, user_id, msg_id, messageCard):
        body = {
            "chat_id": chat_id,
            "user_id": user_id,
            "root_id": msg_id,
            "msg_type": "interactive",
            "card": messageCard,
        }
        req = Request(
            "/open-apis/message/v4/send",
            "POST",
            ACCESS_TOKEN_TYPE_TENANT,
            body,
            output_class=Message,
            request_opts=[set_timeout(3)],
        )
        resp = req.do(self.conf)
        app_logger.debug("send_command_card to %s", chat_id)
        if resp.code == 0:
            return True
        else:
            app_logger.error(
                "send message failed, code:%s, msg:%s, error:%s",
                resp.code,
                resp.msg,
                resp.error,
            )
            return False


if __name__ == "__main__":
    app_config.validate()
    app_settings = Config.new_internal_app_settings_from_env()
    conf = Config(DOMAIN_FEISHU, app_settings)
    message_sender = MessageSender(conf)
