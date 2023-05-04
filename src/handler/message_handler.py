import json

from larksuiteoapi import Config

from feishu.message_sender import MessageSender
from feishu.upload_image import upload_image
from store.chat_history import ChatEvent, get_chat_context_by_user_id
from store.user_prompt import user_prompt
from util.app_config import AppConfig
from util.logger import app_logger
from service.image_configure import ImageConfiguration
from feishu.message_card import handle_image_card
from service.stablediffusion import generate_images

def get_text_message(chat_event: ChatEvent):
    try:
        content = json.loads(chat_event.content)
        if "text" in content:
            return content["text"]
    except json.JSONDecodeError:
        return chat_event.content


def parse_command_line_args(command_line_args):
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


# 根据指令生成不同的消息卡片
def handle_prompt(content):
    inputModel = parse_command_line_args(content)
    # Check if the prompt contains the substring "/help"
    image_cfg = ImageConfiguration()
    image_cfg.update_image_configuration(inputModel, image_cfg)
    image_configuration = image_cfg.get_config_json()
    img_data = generate_images(image_configuration)
    img_key = upload_image(img_data)
    return handle_image_card(image_configuration, img_key)


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
            messageCard = handle_prompt(content['text'])
            return self.message_sender.send_message_card(
                chat_event.user_id, messageCard
            )
        return True
