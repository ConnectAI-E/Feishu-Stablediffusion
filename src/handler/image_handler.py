from util.logger import app_logger
from feishu.data_transfer import upload_image, get_message_resource
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from feishu.message_card import handle_image_card
from service.generate_config import ImageToImageConfig
from feishu.message_sender import message_sender
from PIL import Image
from io import BytesIO
import translators as ts

class ImageHandler:
    def __init__(self) -> None:
        pass

    def img2txt(self, img) -> str:
        result = sd_webui.interrogate(img)
        return result['info']

    # 根据指令生成不同的消息卡片
    def img2img(self, img, prompts):
        gen_cfg = ImageToImageConfig(images=[img])
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        result = sd_webui.img2img(gen_cfg)
        images_key = []
        for img_data in result['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(result['info'], images_key, prompts)

    def handle_image(self, myevent: MyReceiveEvent):
        if myevent.image_key is None:
            return False

        img = get_message_resource(myevent.get_message_id(), myevent.image_key)
        img = Image.open(BytesIO(img))

        if myevent.text is None:
            message_sender.send_text_message(myevent, f"正在以图生文，{sd_webui.queue()}")
            clip_info_en = self.img2txt(img)
            clip_info_cn = ts.translate_text(clip_info_en, translator='alibaba', from_language='en', to_language='zh-cn')
            return message_sender.send_text_message(myevent, f'英文：{clip_info_en}\n中文：{clip_info_cn}')
        else:
            message_sender.send_text_message(myevent, f"正在以图生图，{sd_webui.queue()}")
            messageCard = self.img2img(img, myevent.text)
            return message_sender.send_message_card(myevent, messageCard)
