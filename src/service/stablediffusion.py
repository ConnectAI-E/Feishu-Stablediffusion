# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64, io
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.generate_config import TextToImageConfig, ImageToImageConfig
import webuiapi
from PIL import Image
from io import BytesIO
import re


class StableDiffusionWebUI:
    def __init__(self, webui_host, webui_port=7860, webui_user=None, webui_password=None, use_https=False):
        self.webui_api = webuiapi.WebUIApi(host=webui_host, port=webui_port, use_https=use_https, steps=25)
        if webui_user is not None and webui_password is not None:
            self.webui_api.set_auth(webui_user, webui_password)

        self.txt2img_config = TextToImageConfig()
        self.img2img_config = ImageToImageConfig()

    # def send_api_request(
    #     self,
    #     endpoint,
    #     method='GET',
    #     json=None,
    #     data=None,
    #     params=None,
    # ):
    #     url = f'{self.webui_url}{endpoint}'
    #     auth = (self.webui_user, self.webui_password)
    #     response = requests.request(method=method, url=url, headers=self.headers, json=json, data=data, params=params, auth=auth)
    #     response.raise_for_status()

    #     return response.json()

    # Methods for displaying information
    def helpCard(self):
        cmd_list = [
            {"label": "显示模型列表", "cmd": "/list_models"},
            {"label": "显示采样器列表", "cmd": "/list_samplers"},
            {"label": "显示主机信息", "cmd": "/host_info"},
            {"label": "显示当前队列", "cmd": "/queue"},
            {"label": "显示或设置模型", "cmd": "/model"},
        ]

        a = [
            {"tag": "div", "text": {"content": "**我是SD-BOT，由stablediffusion赋能的图片机器人**", "tag": "lark_md"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"content": "** 获取帮助**\n文本回复\"/help\"", "tag": "lark_md"}},
            {"tag": "hr"},
            {"tag": "div", "text": {"content": "**可用命令列表**", "tag": "lark_md"}},
        ]

        a.extend([{"tag": "div", "text": {"content": "**" + cmd.get('label') + "**\n文本回复\"" + cmd.get('cmd') + "\"", "tag": "lark_md"}} for cmd in cmd_list[:]]),
        print(a)
        help_card = {"elements": a, "header": {"template": "blue", "title": {"content": "🎒需要帮助吗？", "tag": "plain_text"}}}
        return help_card

    def list_models(self):
        models = self.webui_api.get_sd_models()
        models_list_txt = f'共有[{len(models)}]个模型\n'
        for model_info in models:
            model_name = model_info['model_name']
            model_hash = model_info['hash']
            models_list_txt = f'{models_list_txt}模型：{model_name}\t\tHash：{model_hash}\n'

        return models_list_txt

    def list_samplers(self):
        samplers = self.webui_api.get_samplers()
        samplers_list_txt = f'共有[{len(samplers)}]个采样器\n'
        for sampler_info in samplers:
            sampler_name = sampler_info['name']
            samplers_list_txt = f'{samplers_list_txt}采样器：{sampler_name}\n'

        return samplers_list_txt

    def list_upscalers(self):
        upscalers = self.webui_api.get_upscalers()
        upscalers_list_txt = f'共有[{len(upscalers)}]个放大器\n'
        for upscaler_info in upscalers:
            upscaler_name = upscaler_info['name']
            upscalers_list_txt = f'{upscalers_list_txt}放大器：{upscaler_name}\n'

        return upscalers_list_txt

    def refresh_models(self):
        self.webui_api.refresh_checkpoints()
        
    def host_info(self):
        memory_endpoint = 'memory'
        memory = self.webui_api.custom_get(memory_endpoint, True)
        onem = 1024**2
        ram_total = int(memory['ram']['total']) // onem
        ram_free = int(memory['ram']['free']) // onem
        ram_used = int(memory['ram']['used']) // onem
        gpu_ram_total = int(memory['cuda']['system']['total']) // onem
        gpu_ram_free = int(memory['cuda']['system']['free']) // onem
        gpu_ram_used = int(memory['cuda']['system']['used']) // onem

        memory_msg = f'内存：总共[{ram_total}]MB，已用[{ram_used}]MB，剩余[{ram_free}]MB\n显存：总共[{gpu_ram_total}]MB，已用[{gpu_ram_used}]MB，剩余[{gpu_ram_free}]MB'

        return memory_msg

    def queue(self):
        queue = self.webui_api.get_progress()
        queue_size = queue['state']['job_count']
        queue_progress = float(queue['progress']) * 100
        queue_eta = int(queue['eta_relative'])
        queue_msg = f'队列中有[{queue_size}]个任务，当前任务进度[{queue_progress}%]，预计还需要[{queue_eta}]秒'

        return queue_msg

    def set_options(self, options: dict):
        return self.webui_api.set_options(options)

    def get_options(self) -> dict:
        options = self.webui_api.get_options()
        return options

    def set_model(self, model: str):
        self.webui_api.util_set_model(model)

    def get_model(self) -> str:
        model = self.webui_api.util_get_current_model()
        return model

    def parse_prompts_args(self, prompt):
        # 使用正则表达式匹配格式为 "--单词 [值]" 的文本
        matches = re.findall(r'--\b\w+\b\s*\[[^\[\]]+\]', prompt)
        result = {}
        if len(matches) > 0 :
            for match in matches:
                option_match = re.findall(r'--\b\w+\b\s*\[[^\[\]]+\]', match)
            for option in option_match:
                if '--' in option:
                    option_name = option.split('--', 1)[1].split(' ', 1)[0]
                    option_value = option.split('[', 1)[1].split(']', 1)[0]

                    if option_name == 'batch_count':
                        option_name = 'n_iters'
                    elif option_name == 'sampler':
                        option_name = 'sampler_name'

                    result[option_name] = option_value

                    # 将匹配到的文本替换为空字符串
                    prompt = re.sub(re.escape(option), '', prompt)
    
        # 将转换后的字典添加到原字典中
        text_dict = {'prompt': prompt}
        text_dict.update(result)
        return text_dict

    def txt2img(self, gen_cfg: TextToImageConfig):
        gen_cfg.translate_to_english()
        result = self.webui_api.txt2img(**gen_cfg.get_as_json())
        return result.__dict__

    def img2img(self, gen_cfg: ImageToImageConfig):
        gen_cfg.translate_to_english()
        result = self.webui_api.img2img(**gen_cfg.get_as_json())
        return result.__dict__

    def interrogate(self, img):
        result = self.webui_api.interrogate(img)
        return result.__dict__


sd_webui = StableDiffusionWebUI(app_config.WEBUI_HOST, app_config.WEBUI_PORT, app_config.WEBUI_USER, app_config.WEBUI_PASSWORD, app_config.WEBUI_USE_HTTPS)
