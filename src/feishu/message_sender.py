import json
import attr
from larksuiteoapi.api import Request, set_timeout
from larksuiteoapi.service.im.v1 import Service as ImService, model
from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, DOMAIN_FEISHU
from util.event_helper import MyReceiveEvent
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

    def send_text_message(self, myevent: MyReceiveEvent, text, mention_user = False):
        chat_id = myevent.get_chat_id()
        user_id = myevent.get_user_id()
        msg_id = myevent.get_message_id()
        
        body = {
            "chat_id": chat_id,
            "msg_type": "text"
        }
        if mention_user:
            body["content"] = json.dumps({"text": f'<at user_id="{user_id}"></at> \n{text}'})
        else:
            body["content"] = json.dumps({"text": text})
        
        req = Request(
            f"/open-apis/im/v1/messages/{msg_id}/reply",
            "POST",
            ACCESS_TOKEN_TYPE_TENANT,
            body,
            output_class=Message,
            request_opts=[set_timeout(3)],
        )
        resp = req.do(self.conf)
        app_logger.debug("send_text_message:%s", text)
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
    def send_message_card(self, myevent: MyReceiveEvent, messageCard):
        chat_id = myevent.get_chat_id()
        user_id = myevent.get_user_id()
        msg_id = myevent.get_message_id()
        body = {
            "chat_id": chat_id,
            "user_id": user_id,
            "parent_id": msg_id,
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
        
    # 更新消息卡片
    def update_message_card(self, token, messageCard):
        body = {
            "token": token,
            "card": messageCard,
        }
        req = Request(
            "/open-apis/interactive/v1/card/update",
            "POST",
            ACCESS_TOKEN_TYPE_TENANT,
            body,
            output_class=Message,
            request_opts=[set_timeout(3)],
        )
        resp = req.do(self.conf)
        app_logger.debug("update_message_card to %s", token)
        if resp.code == 0:
            return True
        else:
            app_logger.error(
                "update message card failed, code:%s, msg:%s, error:%s",
                resp.code,
                resp.msg,
                resp.error,
            )
            return False

message_sender = MessageSender(feishu_conf)
