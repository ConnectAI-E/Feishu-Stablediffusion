# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.image_configure import ImageConfiguration


def generate_images(gen_cfg):
    url = f"{app_config.WEBUI_URL}/sdapi/v1/txt2img"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    gen_cfg["n_iter"] = gen_cfg["batch_count"]
    gen_cfg["sampler_name"] = gen_cfg["sampler"]
    data = gen_cfg

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=(app_config.WEBUI_USER, app_config.WEBUI_PASSWORD),
    )
    response.raise_for_status()

    rjson = response.json()
    for i in range(len(rjson["images"])):
        rjson["images"][i] = base64.b64decode(rjson["images"][i])

    return rjson


def send_api_request(
    endpoint,
    method="GET",
    headers=None,
    data=None,
    params=None,
    auth=(app_config.WEBUI_USER, app_config.WEBUI_PASSWORD),
):
    url = f"{app_config.WEBUI_URL}{endpoint}"
    response = requests.request(
        method=method, url=url, headers=headers, data=data, params=params, auth=auth
    )
    response.raise_for_status()
    return response.json()
