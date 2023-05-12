import json

from larksuiteoapi import Config

from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import GenerateConfig
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
    def handle_prompt(self, prompt):
        inputModel = sd_webui.parse_prompt_args(prompt)

        # Check if the prompt contains the substring "#" as the negative prompt
        prompts = inputModel["prompt"].split('#', 1)
        if len(prompts) > 1:
            inputModel['prompt'] = prompts[0]
            inputModel['negative_prompt'] = prompts[1]

        # Check if the prompt contains the substring "/help"
        gen_cfg = GenerateConfig()
        gen_cfg.update_configuration(inputModel, gen_cfg)
        image_configuration = gen_cfg.get_config_json()
        images_json = sd_webui.txt2img(image_configuration)
        images_key = []
        for img_data in images_json['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(images_json['info'], images_key, prompt)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent, f"正在生成图片，{sd_webui.queue()}")
        messageCard = self.handle_prompt(myevent.text)

        return message_sender.send_message_card(myevent, messageCard)
