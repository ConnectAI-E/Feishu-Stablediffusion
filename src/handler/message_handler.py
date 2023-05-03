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


def parse_query_string(query_string):
    result = {}
    if query_string:
        pairs = query_string.split("&")
        for pair in pairs:
            key_value = pair.split("=")
            key = key_value[0]
            value = key_value[1] if len(key_value) > 1 else ""
            result[key] = value
    return result


def update_image_configuration(config, image_cfg):
    if "prompt" in config:
        image_cfg.set_prompt(config["prompt"])
    if "model" in config:
        image_cfg.set_model(config["model"])
    if "negative" in config:
        image_cfg.set_negative(config["negative"])
    if "sampler" in config:
        image_cfg.set_sampler(config["sampler"])
    if "step" in config:
        image_cfg.set_step(int(config["step"]))
    if "width" in config:
        image_cfg.set_width(int(config["width"]))
    if "height" in config:
        image_cfg.set_height(int(config["height"]))
    if "batch_count" in config:
        image_cfg.set_batch_count(int(config["batch_count"]))
    if "batch_size" in config:
        image_cfg.set_batch_size(int(config["batch_size"]))
    if "cfg" in config:
        image_cfg.set_cfg(int(config["cfg"]))
    if "seed" in config:
        image_cfg.set_seed(int(config["seed"]))


# 根据指令生成不同的消息卡片
def handle_prompt(content):
    # inputModel = parse_query_string(content)
    # Check if the prompt contains the substring "/help"
    image_cfg = ImageConfiguration()
    # update_image_configuration(inputModel, image_cfg)
    image_cfg.set_prompt(content)
    image_configuration = image_cfg.get_config_json()
    img_data = generate_images(image_cfg)
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
