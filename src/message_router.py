import json
import time
import attr
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from handler.command_handler import CommandHandler
from handler.message_handler import MessageHandler
from util.app_config import app_config
from feishu.feishu_conf import feishu_conf
from util.event_helper import is_mention_bot, get_mention_message, get_pure_message

from util.duplicate_filter import (
    event_is_processed,
    mark_event_processed,
    unmark_event_processed,
)
from util.logger import feishu_message_logger, app_logger

message_handler = MessageHandler(app_config, feishu_conf)
command_handler = CommandHandler(app_config, feishu_conf)

def route_im_message(ctx: Context, conf: Config, event: MessageReceiveEvent) -> Any:
    # ignore request if sender_type is not user
    if event.event.sender.sender_type != "user":
        return
    # ignore request if event_type is not im.message.receive_v1
    if event.header.event_type != "im.message.receive_v1":
        return
    feishu_message_logger.info("Feishu message: %s", attr.asdict(event.event))

    # ignore request if not mention bot in a group
    if event.event.message.chat_type == "group":
        if not is_mention_bot(event):
            return

    if event_is_processed(event):
        app_logger.debug("Skip already processed: %s", attr.asdict(event.event))
        return
    if event.event.message.create_time < (time.time() * 1000 - 10 * 60 * 1000):
        # ignore event if event is 10 minutes old
        app_logger.debug("Skip old event: %s", attr.asdict(event.event))
        return


    try:
        done = False
        message = get_pure_message(event)

        # 带有 / 的消息是命令处理
        if message.startswith("/"):
            done = command_handler.handle_command(event)
        # 否则都认为是图片的 prompt 信息处理
        else:
            done = message_handler.handle_message(event)

        if done:
            mark_event_processed(event)
    except Exception as e:
        app_logger.exception("Failed to handle message: %s", attr.asdict(event.event))
