import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import MessageSender
from util.logger import app_logger
from util.event_helper import get_pure_message
from service.image_configure import ImageConfiguration
from service.stablediffusion import send_api_request
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
        image_configuration = ImageConfiguration()
        command = get_pure_message(event)
        user_id = event.event.sender.sender_id.user_id
        chat_id = event.event.message.chat_id
        msg_id = event.event.message.message_id
        
        if command.startswith("/help"):
            self.message_sender.send_message_card(chat_id, user_id, msg_id, image_configuration.help())
            app_logger.info(f"request /help")
        elif command.startswith("/list_models"):
            models_endpoint = "/sdapi/v1/sd-models"
            models = send_api_request(models_endpoint)
            model_names = [data.get('model_name') for data in models]
            self.message_sender.send_message_card(chat_id, user_id, msg_id, image_configuration.list_models(model_names))
            app_logger.info(f"/sdapi/v1/sd-models")
        elif command.startswith("/list_samplers"):
            models_endpoint = "/sdapi/v1/samplers"
            samplers = send_api_request(models_endpoint)
            samplers_names = [data.get('name') for data in samplers]
            self.message_sender.send_message_card(chat_id, user_id, msg_id, image_configuration.list_sampler(samplers_names))
            app_logger.info(f"/sdapi/v1/samplers")
        elif command.startswith("/queue"):
            models_endpoint = "/queue/status"
            queue = send_api_request(models_endpoint)
            self.message_sender.send_message_card(chat_id, user_id, msg_id, image_configuration.queue(queue))
            app_logger.info(f"/queue")
        else:
            self.message_sender.send_text_message(chat_id, user_id, msg_id, "unknown command")
            app_logger.info("unknown command")
        return True
