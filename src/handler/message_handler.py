import json

from larksuiteoapi import Config

from feishu.message_sender import MessageSender
from service.chatgpt import get_chat_response, get_single_response
from store.chat_history import ChatEvent, get_chat_context_by_user_id
from store.user_prompt import user_prompt
from util.app_config import AppConfig
from util.logger import app_logger


def get_text_message(chat_event: ChatEvent):
    try:
        content = json.loads(chat_event.content)
        if "text" in content:
            return content["text"]
    except json.JSONDecodeError:
        return chat_event.content


class MyMessageEventHandler:
    def __init__(self, app_config: AppConfig, conf: Config):
        if not app_config:
            raise Exception("app_config is required")
        if not conf:
            raise Exception("conf is required")
        self.conf = conf
        self.app_config = app_config
        self.message_sender = MessageSender(self.conf)

    def handle_message(self, chat_event: ChatEvent):
        content = json.loads(chat_event.content)
        # check if the message is already handled
        if "text" in content:
            # get history
            db_history = get_chat_context_by_user_id(chat_event.user_id)
            prompt = user_prompt.read_prompt(chat_event.user_id)
            extra_args = {"prompt": prompt} if prompt else {}
            if len(db_history) == 0:
                return self.message_sender.send_text_message(
                    chat_event.sender_user_id, get_chat_response([{"role": "user", "content": content["text"]}], **extra_args))
            else:
                gpt_history = [{"role": "assistant", "content": get_text_message(x)} if x.sender_user_id == "assistant" else {
                    "role": "user", "content": get_text_message(x)} for x in db_history]
                response = get_chat_response(gpt_history, **extra_args)
                return self.message_sender.send_text_message(
                    chat_event.user_id, response,  chat_event.open_id)
        return True
