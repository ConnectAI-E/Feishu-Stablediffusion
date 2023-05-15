# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64, io
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.generate_config import TextToImageConfig
import webuiapi
from PIL import Image
from io import BytesIO


class StableDiffusionWebUI:
    def __init__(self, webui_host, webui_port=7860, webui_user=None, webui_password=None):
        self.webui_api = webuiapi.WebUIApi(webui_host, webui_port)
        if webui_user is not None and webui_password is not None:
            self.webui_api.set_auth(webui_user, webui_password)

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
            {"label": "显示最后n条日志", "cmd": "/log"},
            {"label": "显示或设置模型", "cmd": "/model"},
            {"label": "显示或设置反提示词", "cmd": "/negative"},
            {"label": "显示或设置采样器", "cmd": "/sampler"},
            {"label": "显示或设置步数", "cmd": "/steps"},
            {"label": "显示或设置宽度", "cmd": "/width"},
            {"label": "显示或设置高度", "cmd": "/height"},
            {"label": "显示或设置批次数", "cmd": "/batch_count"},
            {"label": "显示或设置批次大小", "cmd": "/batch_size"},
            {"label": "显示或设置CFG", "cmd": "/cfg"},
            {"label": "显示或设置种子'", "cmd": "/seed"},
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
        return models

    def list_samplers(self):
        samplers = self.webui_api.get_samplers()
        return samplers

    def host_info(self):
        memory_endpoint = 'memory'
        memory = self.webui_api.custom_get(memory_endpoint, True)
        return memory

    def queue(self):
        queue = self.webui_api.get_progress()
        queue_size = queue['state']['job_count']
        queue_progress = float(queue['progress'])*100
        queue_eta = int(queue['eta_relative'])
        queue_msg = f'队列中有[{queue_size}]个任务，当前任务进度[{queue_progress}%]，预计还需要[{queue_eta}]秒'

        return queue_msg

    def log(self, n=5):
        return 'logs\n' * n

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
        result = {}
        if prompt:
            # Split the command line args into individual tokens
            tokens = prompt.split()
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token.startswith("--"):
                    # This is an option
                    option_name = token[2:]
                    if option_name == 'batch_count':
                        option_name = 'n_iters'
                    elif option_name == 'sampler':
                        option_name = 'sampler_name'
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                        # The option has a value
                        option_value = tokens[i + 1]
                        result[option_name] = option_value
                        i += 1
                    else:
                        # The option does not have a value
                        result[option_name] = True
                else:
                    # This is an argument
                    if "prompt" in result:
                        # Append to the existing prompt
                        result["prompt"] += " " + token
                    else:
                        # Create a new prompt
                        result["prompt"] = token
                i += 1
            
            prompts = result["prompt"].split('#', 1)
            if len(prompts) > 1:
                result['prompt'] = prompts[0]
                result['negative_prompt'] = prompts[1]

        return result

    def txt2img(self, gen_cfg):
        result = self.webui_api.txt2img(**gen_cfg.get_as_json())
        return result.__dict__

    def img2img(self, gen_cfg):
        result = self.webui_api.img2img(**gen_cfg.get_as_json())
        return result.__dict__

    def interrogate(self, img):
        result = self.webui_api.interrogate(img)
        return result.__dict__


sd_webui = StableDiffusionWebUI(app_config.WEBUI_HOST, app_config.WEBUI_PORT, app_config.WEBUI_USER, app_config.WEBUI_PASSWORD)
