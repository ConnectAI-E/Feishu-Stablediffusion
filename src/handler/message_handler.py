import json

from larksuiteoapi import Config

from feishu.message_sender import MessageSender
from feishu.upload_image import upload_image
from util.app_config import AppConfig
from util.logger import app_logger
from util.event_helper import get_pure_message
from service.generate_config import GenerateConfig
from feishu.message_card import handle_image_card
from service.stablediffusion import sd_webui


class MessageHandler:
    def __init__(self, app_config: AppConfig, conf: Config):
        if not app_config:
            raise Exception("app_config is required")
        if not conf:
            raise Exception("conf is required")
        self.conf = conf
        self.app_config = app_config
        self.message_sender = MessageSender(self.conf)

    def parse_command_line_args(self, command_line_args):
        result = {}
        if command_line_args:
            # Split the command line args into individual tokens
            tokens = command_line_args.split()
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token.startswith("--"):
                    # This is an option
                    option_name = token[2:]
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                        # The option has a value
                        option_value = tokens[i + 1]
                        result[option_name] = option_value
                        i += 1
                    else:
                        # The option does not have a value
                        result[option_name] = ""
                else:
                    # This is an argument
                    if "prompt" in result:
                        # Append to the existing prompt
                        result["prompt"] += " " + token
                    else:
                        # Create a new prompt
                        result["prompt"] = token
                i += 1
        return result

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        messageCard["open_ids"] = [openId]
        return self.message_sender.update_message_card(token, messageCard)

    # 根据指令生成不同的消息卡片
    def handle_prompt(self, prompt):
        inputModel = self.parse_command_line_args(prompt)
        # Check if the prompt contains the substring "/help"
        image_cfg = GenerateConfig()
        image_cfg.update_image_configuration(inputModel, image_cfg)
        image_configuration = image_cfg.get_config_json()
        images_json = sd_webui.generate_images(image_configuration)
        images_key = []
        for img_data in images_json['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(images_json['info'], images_key, prompt)

    def handle_message(self, event):
        user_id = event.event.sender.sender_id.user_id
        chat_id = event.event.message.chat_id
        msg_id = event.event.message.message_id
        
        text = get_pure_message(event)
        messageCard = self.handle_prompt(text)

        return self.message_sender.send_message_card(chat_id, user_id, msg_id, messageCard)
