import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import MessageSender
from util.logger import app_logger
from util.event_helper import get_pure_message
from service.stablediffusion import sd_webui


class CommandHandler:
    def __init__(self, app_config: AppConfig, conf: Config):
        if not app_config:
            raise Exception("app_config is required")
        if not conf:
            raise Exception("conf is required")
        self.app_config = app_config
        self.conf = conf
        self.message_sender = MessageSender(self.conf)

    def handle_command(self, event):
        command = get_pure_message(event)
        user_id = event.event.sender.sender_id.user_id
        chat_id = event.event.message.chat_id
        msg_id = event.event.message.message_id

        if command.startswith("/help"):
            self.message_sender.send_text_message(chat_id, user_id, msg_id, sd_webui.help())
            app_logger.info(f"request /help")
        elif command.startswith("/list_models"):
            self.message_sender.send_text_message(chat_id, user_id, msg_id, sd_webui.list_models())
            app_logger.info(f"/sdapi/v1/sd-models")
        elif command.startswith("/list_samplers"):
            self.message_sender.send_text_message(chat_id, user_id, msg_id, sd_webui.list_samplers())
            app_logger.info(f"/sdapi/v1/samplers")
        elif command.startswith("/host_info"):
            self.message_sender.send_text_message(chat_id, user_id, msg_id, sd_webui.host_info())
            app_logger.info(f"/sdapi/v1/samplers")
        elif command.startswith("/queue"):
            self.message_sender.send_text_message(chat_id, user_id, msg_id, sd_webui.queue())
            app_logger.info(f"/queue")
        else:
            self.message_sender.send_text_message(chat_id, user_id, msg_id, "unknown command")
            app_logger.info("unknown command")
        return True
