# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.image_configure import ImageConfiguration

def generate_images(gen_cfg: ImageConfiguration):
    url = f"{app_config.WEBUI_URL}/sdapi/v1/txt2img"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "enable_hr": False,
        "denoising_strength": 0,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": "",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "prompt": gen_cfg.prompt,
        "styles": [],
        "seed": gen_cfg.seed,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": gen_cfg.sampler,
        "batch_size": gen_cfg.batch_size,
        "n_iter": gen_cfg.batch_count,
        "steps": gen_cfg.step,
        "cfg_scale": gen_cfg.cfg,
        "width": gen_cfg.width,
        "height": gen_cfg.height,
        "restore_faces": True,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "negative_prompt": "",
        "eta": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "Euler",
        "script_name": "",
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {},
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=(app_config.WEBUI_USER, app_config.WEBUI_PASSWORD),
    )
    img_bytes = base64.b64decode(response.json()["images"][0])
    return img_bytes
