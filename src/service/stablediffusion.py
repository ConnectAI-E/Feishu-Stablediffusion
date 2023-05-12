# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64, io
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.generate_config import GenerateConfig
from PIL import Image


class StableDiffusionWebUI:
    def __init__(
        self,
        webui_url=app_config.WEBUI_URL,
        headers={'accept': 'application/json', 'Content-Type': 'application/json'},
        webui_user=app_config.WEBUI_USER,
        webui_password=app_config.WEBUI_PASSWORD,
    ):
        self.webui_url = webui_url.strip('/')
        self.headers = headers
        self.webui_user = webui_user
        self.webui_password = webui_password

    def send_api_request(
        self,
        endpoint,
        method='GET',
        json=None,
        data=None,
        params=None,
    ):
        url = f'{self.webui_url}{endpoint}'
        auth = (self.webui_user, self.webui_password)
        response = requests.request(method=method, url=url, headers=self.headers, json=json, data=data, params=params, auth=auth)
        response.raise_for_status()

        return response.json()

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
        models_endpoint = "/sdapi/v1/sd-models"
        models = self.send_api_request(models_endpoint)
        return models

    def list_samplers(self):
        models_endpoint = '/sdapi/v1/samplers'
        samplers = sd_webui.send_api_request(models_endpoint)
        return samplers

    def host_info(self):
        memory_endpoint = '/sdapi/v1/memory'
        memory = self.send_api_request(memory_endpoint)
        return memory

    def queue(self):
        queue_endpoint = '/queue/status'
        queue = sd_webui.send_api_request(queue_endpoint)
        queue_size = queue['queue_size']
        queue_eta = queue['queue_eta']
        queue_msg = f'队列中有[{queue_size}]个任务，预计还需要[{queue_eta}]秒'
        return queue_msg

    def log(self, n=5):
        if n is None:
            n = self.log_size
        print('Last {} log messages: ...')  # TODO: display last n log messages

    def set_options(self, options: dict):
        options_endpoint = '/sdapi/v1/options'
        self.send_api_request(options_endpoint, method='POST', json=options)
        sd_logger.info(f'Set options {options}')

    def get_options(self) -> dict:
        options_endpoint = '/sdapi/v1/options'
        options = self.send_api_request(options_endpoint)
        return options

    def set_model(self, model: str):
        option_model = {'sd_model_checkpoint': model}
        self.set_options(option_model)
        sd_logger.info(f'Switched to model {model}')

    def get_model(self) -> str:
        model = self.get_options()['sd_model_checkpoint']
        return model

    def parse_prompt_args(self, prompt):
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
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                        # The option has a value
                        option_value = tokens[i + 1]
                        result[option_name] = option_value
                        i += 1
                    else:
                        # The option does not have a value
                        result[option_name] = ""
                else:
                    # This is an argument
                    if "prompt" in result:
                        # Append to the existing prompt
                        result["prompt"] += " " + token
                    else:
                        # Create a new prompt
                        result["prompt"] = token
                i += 1
        return result

    def txt2img(self, gen_cfg):
        endpoint = '/sdapi/v1/txt2img'
        gen_cfg['n_iter'] = gen_cfg['batch_count']
        gen_cfg['sampler_name'] = gen_cfg['sampler']
        rjson = self.send_api_request(endpoint, method='POST', json=gen_cfg)

        for i in range(len(rjson['images'])):
            rjson['images'][i] = self.base64_img(rjson['images'][i])

        return rjson

    def img_base64(self, img):
        img_base64 = base64.b64encode(img).decode(encoding='utf-8')
        return 'data:image/png;base64,' + str(img_base64)

    def base64_img(self, img_base64):
        img = base64.b64decode(img_base64)
        return img

    def img2img(self, img, gen_cfg):
        endpoint = '/sdapi/v1/img2img'
        gen_cfg['n_iter'] = gen_cfg['batch_count']
        gen_cfg['sampler_name'] = gen_cfg['sampler']
        gen_cfg['init_images'] = [self.img_base64(img)]
        rjson = self.send_api_request(endpoint, method='POST', json=gen_cfg)

        for i in range(len(rjson['images'])):
            rjson['images'][i] = self.base64_img(rjson['images'][i])

        return rjson

    def interrogate(self, img):
        endpoint = '/sdapi/v1/interrogate'
        img_cfg = {
            'image': self.img_base64(img),
        }
        rjson = self.send_api_request(endpoint, method='POST', json=img_cfg)

        return rjson


sd_webui = StableDiffusionWebUI()
