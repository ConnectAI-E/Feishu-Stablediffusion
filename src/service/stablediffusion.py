# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.image_configure import ImageConfiguration

def generate_images(gen_cfg):
    url = f"{app_config.WEBUI_URL}/sdapi/v1/txt2img"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    gen_cfg['n_iter'] = gen_cfg['batch_count']
    gen_cfg['sampler_name'] = gen_cfg['sampler']
    data = gen_cfg

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=(app_config.WEBUI_USER, app_config.WEBUI_PASSWORD),
    )
    img_bytes = base64.b64decode(response.json()["images"][0])
    return img_bytes
