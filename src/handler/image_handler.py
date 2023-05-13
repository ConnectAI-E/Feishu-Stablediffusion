from util.logger import app_logger
from feishu.data_transfer import upload_image, get_image
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from feishu.message_card import handle_image_card
from service.generate_config import GenerateConfig
from feishu.message_sender import message_sender


class ImageHandler:
    def __init__(self) -> None:
        pass

    def img2txt(self, img) -> str:
        txt = sd_webui.interrogate(img)
        return txt

    # 根据指令生成不同的消息卡片
    def img2img(self, img, prompt):
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
        images_json = sd_webui.img2img(img, image_configuration)
        images_key = []
        for img_data in images_json['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(images_json['info'], images_key, prompt)

    def handle_image(self, myevent: MyReceiveEvent):
        if myevent.image is None:
            return False

        img = get_image(myevent.get_message_id(), myevent.image)

        if myevent.text is None:
            message_sender.send_text_message(myevent, f"正在以图生文，{sd_webui.queue()}")
            messageCard = self.img2txt(img)
        else:
            message_sender.send_text_message(myevent, f"正在以图生图，{sd_webui.queue()}")
            messageCard = self.img2img(img, myevent.text)

        return message_sender.send_message_card(myevent, messageCard)
