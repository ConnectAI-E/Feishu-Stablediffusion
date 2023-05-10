# Note: The openai-python library support for Azure OpenAI is in preview.
import requests, base64
from util.app_config import app_config
from util.logger import sd_logger, app_logger
from service.generate_config import GenerateConfig


class StableDiffusionWebUI:
    def __init__(
        self,
        webui_url=app_config.WEBUI_URL,
        headers={"accept": "application/json", "Content-Type": "application/json"},
        webui_user=app_config.WEBUI_USER,
        webui_password=app_config.WEBUI_PASSWORD,
    ):
        self.webui_url = webui_url.strip("/")
        self.headers = headers
        self.webui_user = webui_user
        self.webui_password = webui_password

    def send_api_request(
        self,
        endpoint,
        method="GET",
        data=None,
        params=None,
    ):
        url = f"{self.webui_url}{endpoint}"
        auth = (self.webui_user, self.webui_password)
        response = requests.request(method=method, url=url, headers=self.headers, data=data, params=params, auth=auth)
        response.raise_for_status()

        return response.json()

    # Methods for displaying information
    def help(self):
        cmd_list = [
            '信息显示类命令：',
            '/help          显示帮助',
            '/list_models   显示模型列表',
            '/list_samplers 显示采样器列表',
            '/host_info     显示主机信息',
            '/queue         显示当前队列',
            '/log n         显示最后n条日志',
            '\n状态显示与设置类命令：',
            '/model         显示或设置模型',
            '/negative      显示或设置反提示词',
            '/sampler       显示或设置采样器',
            '/steps         显示或设置步数',
            '/width         显示或设置宽度',
            '/height        显示或设置高度',
            '/batch_count   显示或设置批次数',
            '/batch_size    显示或设置批次大小',
            '/cfg           显示或设置CFG',
            '/seed          显示或设置种子',
        ]
        return cmd_list

    def list_models(self):
        models_endpoint = "/sdapi/v1/sd-models"
        models = self.send_api_request(models_endpoint)
        return models

    def list_samplers(self):
        models_endpoint = "/sdapi/v1/samplers"
        samplers = sd_webui.send_api_request(models_endpoint)
        return samplers

    def host_info(self):
        memory_endpoint = "/sdapi/v1/memory"
        memory = self.send_api_request(memory_endpoint)
        return memory

    def queue(self):
        queue_endpoint = "/queue/status"
        queue = sd_webui.send_api_request(queue_endpoint)
        return queue

    def log(self, n=5):
        if n is None:
            n = self.log_size
        print('Last {} log messages: ...')  # TODO: display last n log messages

    def generate_images(self, gen_cfg):
        endpoint = f'{self.webui_url}/sdapi/v1/txt2img'
        gen_cfg["n_iter"] = gen_cfg["batch_count"]
        gen_cfg["sampler_name"] = gen_cfg["sampler"]
        response = requests.post(
            endpoint,
            headers=self.headers,
            json=gen_cfg,
            auth=(self.webui_user, self.webui_password),
        )
        response.raise_for_status()
        rjson = response.json()
        for i in range(len(rjson["images"])):
            rjson["images"][i] = base64.b64decode(rjson["images"][i])

        return rjson


sd_webui = StableDiffusionWebUI()
