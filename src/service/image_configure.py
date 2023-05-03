import json
from feishu.message_card import LIST_INFO_CARD, handle_list_info_card


class ImageConfiguration:
    def __init__(self):
        self.prompt = ""
        self.model = "SD"  # default values
        self.negative = ""
        self.sampler = "Euler a"
        self.step = 20
        self.width = 512
        self.height = 512
        self.batch_count = 1
        self.batch_size = 1
        self.cfg = 7
        self.seed = -1
        self.log_size = 5  # default number of logs to display

    # Methods for displaying information
    def help(self):
        list = ['help', 'list', 'list models', 'list samplers', 'host info', 'queue', 'log', 'set model', 'set negative', 'set sampler', 'set step', 'set width', 'set height', 'set batch count', 'set batch size', 'set cfg', 'set seed']
        return handle_list_info_card(LIST_INFO_CARD, list)

    def list_models(self):
        print("Available models: ...") # TODO: add list of models

    def list_sampler(self):
        print("Available samplers: ...") # TODO: add list of samplers

    def host_info(self):
        print("System information: ...") # TODO: display system information

    def queue(self):
        print("Queue length: ...") # TODO: display queue length

    def log(self, n=None):
        if n is None:
            n = self.log_size
        print("Last {} log messages: ...") # TODO: display last n log messages

    def error(self, message):
        list = [message]
        return handle_list_info_card(LIST_INFO_CARD, list)

    # Methods for setting configuration values
    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_model(self, model):
        self.model = model

    def set_negative(self, negative):
        self.negative = negative

    def set_sampler(self, sampler):
        self.sampler = sampler

    def set_step(self, step):
        self.step = step

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_batch_count(self, batch_count):
        self.batch_count = batch_count

    def set_batch_size(self, batch_size):
        self.batch_size = batch_size

    def set_cfg(self, cfg):
        self.cfg = cfg

    def set_seed(self, seed):
        self.seed = seed

    # Method to return current configuration as a JSON string
    def get_config_json(self):
        config = {
            "prompt": self.prompt,
            "model": self.model,
            "negative": self.negative,
            "sampler": self.sampler,
            "step": self.step,
            "width": self.width,
            "height": self.height,
            "batch_count": self.batch_count,
            "batch_size": self.batch_size,
            "cfg": self.cfg,
            "seed": self.seed
        }
        return json.dumps(config)