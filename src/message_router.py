import json
import time
import attr
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from handler.command_handler import CommandHandler
from handler.message_handler import MessageHandler
from handler.image_handler import ImageHandler

from util.event_helper import MyReceiveEvent
from feishu.message_sender import message_sender

from util.duplicate_filter import (
    event_is_processed,
    mark_event_processed,
    unmark_event_processed,
)
from util.logger import feishu_logger, app_logger

message_handler = MessageHandler()
command_handler = CommandHandler()
image_handler = ImageHandler()


def route_im_message(ctx: Context, conf: Config, event: MessageReceiveEvent) -> Any:
    # ignore request if sender_type is not user
    if event.event.sender.sender_type != 'user':
        return
    # ignore request if event_type is not im.message.receive_v1
    if event.header.event_type != 'im.message.receive_v1':
        return

    if event_is_processed(event):
        app_logger.debug('Skip already processed: %s', attr.asdict(event.event))
        return
    if event.event.message.create_time < (time.time() * 1000 - 10 * 60 * 1000):
        # ignore event if event is 10 minutes old
        app_logger.debug('Skip old event: %s', attr.asdict(event.event))
        return

    myevent = MyReceiveEvent(event.event)
    # ignore request if event is not group chat or not mentioned bot
    if myevent.is_group_chat() and not myevent.is_mentioned_bot():
        return

    feishu_logger.info('Feishu message: %s', attr.asdict(event))

    # ignore request if event has no content
    if not myevent.has_content():
        message_sender.send_text_message(myevent, '请发送包含文字或图片的消息')
        feishu_logger.info('Skip event with no content:')
        return

    done = False

    try:
        if myevent.image_key is None:
            if myevent.text is not None:
                if myevent.is_command_msg():
                    done = command_handler.handle_command(myevent)
                else:
                    done = message_handler.handle_message(myevent)
        else:
            done = image_handler.handle_image(myevent)

        if not done:
            message_sender.send_text_message(myevent, '生成失败！', True)

    except Exception as e:
        message_sender.send_text_message(myevent, f'发生错误: {e}', True)

    finally:
        mark_event_processed(event)
