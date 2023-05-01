
import json
import time
import attr
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from store.chat_history import ChatEvent, append_chat_event, clean_chat
from handler.command_handler import CommandHandler
from handler.message_handler import MyMessageEventHandler
from util.app_config import app_config
from feishu.feishu_conf import feishu_conf
from util.duplicate_filter import bot_event_is_processed, event_is_processed, mark_bot_event_processed, mark_event_processed
from util.logger import feishu_message_logger, app_logger

message_handler = MyMessageEventHandler(app_config, feishu_conf)
command_handler = CommandHandler(app_config, feishu_conf)

def route_bot_message(body):
    # body.action.value
    if "action" not in body or "value" not in body["action"]:
        return
    if "user_id" not in body:
        return
    if "token" not in body:
        return
    if bot_event_is_processed(body):
        app_logger.debug("Skip already processed: %s", body)
        return
    command_handler.handle_botmessage(body)
    mark_bot_event_processed(body)

def route_im_message(ctx: Context, conf: Config, event: MessageReceiveEvent) -> Any:
    # ignore request if sender_type is not user
    if event.event.sender.sender_type != "user":
        return
    # ignore request if event_type is not im.message.receive_v1
    if event.header.event_type != "im.message.receive_v1":
        return
    feishu_message_logger.info("Feishu message: %s", attr.asdict(event.event))
    # if message content text starts with /, then it is a command
    json_content = json.loads(event.event.message.content)

    if event_is_processed(event):
        app_logger.debug("Skip already processed: %s",
                         attr.asdict(event.event))
        return
    if event.event.message.create_time < (time.time() * 1000 - 10 * 60 * 1000):
        # ignore event if event is 10 minutes old
        app_logger.debug("Skip old event: %s", attr.asdict(event.event))
        return

    if "text" in json_content and json_content["text"].startswith("/"):
        if command_handler.handle_message(event):
            mark_event_processed(event)
    else:
        chat_event = ChatEvent(**{
            "open_id": event.event.sender.sender_id.open_id,
            "user_id": event.event.sender.sender_id.user_id,
            "chat_id": event.event.message.chat_id,
            "chat_type": event.event.message.chat_type,
            "message_id": event.event.message.message_id,
            "message_type": event.event.message.message_type,
            "content": event.event.message.content,
            "create_time": event.event.message.create_time,
            "sender_user_id": event.event.sender.sender_id.user_id
        })
        append_chat_event(chat_event)
        mark_event_processed(event)
        if not message_handler.handle_message(chat_event):
            unmark_event_processed(event)
