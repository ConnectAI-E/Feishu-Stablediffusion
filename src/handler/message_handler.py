import json

from larksuiteoapi import Config

from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import TextToImageConfig
from feishu.message_card import handle_image_card
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent

class MessageHandler:
    def __init__(self):
        pass

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        messageCard["open_ids"] = [openId]
        return message_sender.update_message_card(token, messageCard)

    # 根据指令生成不同的消息卡片
    def handle_prompt(self, prompts):
        gen_cfg = TextToImageConfig()
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        result = sd_webui.txt2img(gen_cfg)
        images_key = []
        for img_data in result['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(result['info'], images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent, f"当前{sd_webui.queue()}")
        messageCard = self.handle_prompt(myevent.text)

        return message_sender.send_message_card(myevent, messageCard)
