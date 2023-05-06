import json
import time
import attr
from larksuiteoapi.api import Request, set_timeout
from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_FEISHU
from util.app_config import app_config
from util.logger import app_logger

@attr.s
class Message(object):
    message_id = attr.ib(type=str)  # type: ignore


class MessageSender:
    def __init__(self, conf: Config):
        if not conf:
            raise Exception("conf is required")
        self.conf = conf

    def send_text_message(self, user_id, msg, append=True):
        body = {
            "user_id": user_id,
            "msg_type": "text",
            "content": {
                "text": msg
            }
        }
        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                      output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)
        app_logger.debug("send_text_message:%s", msg)
        if resp.code == 0:
            # store the message in the chat history
            return True
        else:
            app_logger.error(
                "send message failed, code:%s, msg:%s, error:%s", resp.code, resp.msg, resp.error)
            return False
    # 发送消息卡片
    def send_message_card(self, user_id, messageCard):
        body = {
            "user_id": user_id,
            "msg_type": "interactive",
            "card": messageCard
        }
        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                      output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)
        app_logger.debug("send_command_card to %s", user_id)
        if resp.code == 0:
            return True
        else:
            app_logger.error(
                "send message failed, code:%s, msg:%s, error:%s", resp.code, resp.msg, resp.error)
            return False

    def send_card(self, user_id, card):
        body = {
            "user_id": user_id,
            "msg_type": "interactive",
            "card": card
        }
        req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                      output_class=Message, request_opts=[set_timeout(3)])
        resp = req.do(self.conf)
        app_logger.debug("send_command_card to %s", user_id)
        if resp.code == 0:
            return True
        else:
            app_logger.error(
                "send message failed, code:%s, msg:%s, error:%s", resp.code, resp.msg, resp.error)
            return False


if __name__ == '__main__':
    app_config.validate()
    app_settings = Config.new_internal_app_settings_from_env()
    conf = Config(DOMAIN_FEISHU, app_settings)
    message_sender = MessageSender(conf)
