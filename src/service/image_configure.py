import json
from feishu.message_card import LIST_INFO_CARD, handle_list_info_card


class ImageConfiguration:
    def __init__(self):
        self.prompt = "1girl"
        self.model = "SD"
        self.negative = ""
        self.sampler = "Euler a"
        self.step = 50
        self.width = 512
        self.height = 512
        self.batch_count = 2
        self.batch_size = 2
        self.cfg = 7
        self.seed = -1
        self.log_size = 5
        self.enable_hr = False
        self.denoising_strength = 0
        self.firstphase_width = 0
        self.firstphase_height = 0
        self.hr_scale = 2
        self.hr_upscaler = "string"
        self.hr_second_pass_steps = 0
        self.hr_resize_x = 0
        self.hr_resize_y = 0
        self.styles = []
        self.subseed = -1
        self.subseed_strength = 0
        self.seed_resize_from_h = -1
        self.seed_resize_from_w = -1
        self.tiling = False
        self.do_not_save_samples = False
        self.do_not_save_grid = False
        self.restore_faces = False
        self.negative_prompt = "string"
        self.eta = 0
        self.s_churn = 0
        self.s_tmax = 0
        self.s_tmin = 0
        self.s_noise = 1
        self.override_settings = {}
        self.override_settings_restore_afterwards = True
        self.script_args = []
        self.sampler_index = ""
        self.script_name = ""
        self.send_images = True
        self.save_images = False
        self.alwayson_scripts = {}

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

    # Methods for getting configuration values
    def get_prompt(self):
        return self.prompt
    
    def get_model(self):
        return self.model
    
    def get_negative(self):
        return self.negative
    
    def get_sampler(self):
        return self.sampler
    
    def get_step(self):
        return self.step
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_batch_count(self):
        return self.batch_count
    
    def get_batch_size(self):
        return self.batch_size
    
    def get_cfg(self):
        return self.cfg
    
    def get_seed(self):
        return self.seed
    
    def get_enable_hr(self):
        return self.enable_hr
    
    def get_denoising_strength(self):
        return self.denoising_strength
    
    def get_firstphase_width(self):
        return self.firstphase_width
    
    def get_firstphase_height(self):
        return self.firstphase_height
    
    def get_hr_scale(self):
        return self.hr_scale
    
    def get_hr_upscaler(self):
        return self.hr_upscaler
    
    def get_hr_second_pass_steps(self):
        return self.hr_second_pass_steps
    
    def get_hr_resize_x(self):
        return self.hr_resize_x
    
    def get_hr_resize_y(self):
        return self.hr_resize_y
    
    def get_styles(self):
        return self.styles
    
    def get_subseed(self):
        return self.subseed
    
    def get_subseed_strength(self):
        return self.subseed_strength
    
    def get_seed_resize_from_h(self):
        return self.seed_resize_from_h
    
    def get_seed_resize_from_w(self):
        return self.seed_resize_from_w
    
    def get_tiling(self):
        return self.tiling
    
    def get_do_not_save_samples(self):
        return self.do_not_save_samples
    
    def get_do_not_save_grid(self):
        return self.do_not_save_grid
    
    def get_restore_faces(self):
        return self.restore_faces
    
    def get_negative_prompt(self):
        return self.negative_prompt
    
    def get_eta(self):
        return self.eta
    
    def get_s_churn(self):
        return self.s_churn
    
    def get_s_tmax(self):
        return self.s_tmax
    
    def get_s_tmin(self):
        return self.s_tmin
    
    def get_s_noise(self):
        return self.s_noise
    
    def get_override_settings(self):
        return self.override_settings
    
    def get_override_settings_restore_afterwards(self):
        return self.override_settings_restore_afterwards
    
    def get_script_args(self):
        return self.script_args
    
    def get_sampler_index(self):
        return self.sampler_index
    
    def get_script_name(self):
        return self.script_name
    
    def get_send_images(self):
        return self.send_images
    
    def get_save_images(self):
        return self.save_images
    
    def get_alwayson_scripts(self):
        return self.alwayson_scripts

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

    def set_enable_hr(self, enable_hr):
        self.enable_hr = enable_hr

    def set_denoising_strength(self, denoising_strength):
        self.denoising_strength = denoising_strength

    def set_firstphase_width(self, firstphase_width):
        self.firstphase_width = firstphase_width

    def set_firstphase_height(self, firstphase_height):
        self.firstphase_height = firstphase_height

    def set_hr_scale(self, hr_scale):
        self.hr_scale = hr_scale

    def set_hr_upscaler(self, hr_upscaler):
        self.hr_upscaler = hr_upscaler

    def set_hr_second_pass_steps(self, hr_second_pass_steps):
        self.hr_second_pass_steps = hr_second_pass_steps

    def set_hr_resize_x(self, hr_resize_x):
        self.hr_resize_x = hr_resize_x

    def set_hr_resize_y(self, hr_resize_y):
        self.hr_resize_y = hr_resize_y

    def set_styles(self, styles):
        self.styles = styles

    def set_subseed(self, subseed):
        self.subseed = subseed

    def set_subseed_strength(self, subseed_strength):
        self.subseed_strength = subseed_strength

    def set_seed_resize_from_h(self, seed_resize_from_h):
        self.seed_resize_from_h = seed_resize_from_h

    def set_seed_resize_from_w(self, seed_resize_from_w):
        self.seed_resize_from_w = seed_resize_from_w

    def set_tiling(self, tiling):
        self.tiling = tiling

    def set_do_not_save_samples(self, do_not_save_samples):
        self.do_not_save_samples = do_not_save_samples

    def set_do_not_save_grid(self, do_not_save_grid):
        self.do_not_save_grid = do_not_save_grid

    def set_restore_faces(self, restore_faces):
        self.restore_faces = restore_faces

    def set_negative_prompt(self, negative_prompt):
        self.negative_prompt = negative_prompt

    def set_eta(self, eta):
        self.eta = eta

    def set_s_churn(self, s_churn):
        self.s_churn = s_churn

    def set_s_tmax(self, s_tmax):
        self.s_tmax = s_tmax

    def set_s_tmin(self, s_tmin):
        self.s_tmin = s_tmin

    def set_s_noise(self, s_noise):
        self.s_noise = s_noise

    def set_override_settings(self, override_settings):
        self.override_settings = override_settings

    def set_override_settings_restore_afterwards(self, override_settings_restore_afterwards):
        self.override_settings_restore_afterwards = override_settings_restore_afterwards

    def set_script_args(self, script_args):
        self.script_args = script_args

    def set_sampler_index(self, sampler_index):
        self.sampler_index = sampler_index

    def set_script_name(self, script_name):
        self.script_name = script_name

    def set_send_images(self, send_images):
        self.send_images = send_images

    def set_save_images(self, save_images):
        self.save_images = save_images

    def set_alwayson_scripts(self, alwayson_scripts):
        self.alwayson_scripts = alwayson_scripts
    
    def update_image_configuration(self, config, image_cfg):
        if "prompt" in config:
            image_cfg.set_prompt(config["prompt"])
        if "model" in config:
            image_cfg.set_model(config["model"])
        if "negative" in config:
            image_cfg.set_negative(config["negative"])
        if "sampler" in config:
            config.set()
            image_cfg.set_sampler(config["sampler"])
        if "step" in config:
            image_cfg.set_step(config["step"])
        if "width" in config:
            image_cfg.set_width(config["width"])
        if "height" in config:
            image_cfg.set_height(config["height"])
        if "batch_count" in config:
            image_cfg.set_batch_count(config["batch_count"])
        if "batch_size" in config:
            image_cfg.set_batch_size(config["batch_size"])
        if "cfg" in config:
            image_cfg.set_cfg(config["cfg"])
        if "seed" in config:
            image_cfg.set_seed(config["seed"])
        if "enable_hr" in config:
            image_cfg.set_enable_hr(config["enable_hr"])
        if "denoising_strength" in config:
            image_cfg.set_denoising_strength(config["denoising_strength"])
        if "firstphase_width" in config:
            image_cfg.set_firstphase_width(config["firstphase_width"])
        if "firstphase_height" in config:
            image_cfg.set_firstphase_height(config["firstphase_height"])
        if "hr_scale" in config:
            image_cfg.set_hr_scale(config["hr_scale"])
        if "hr_upscaler" in config:
            image_cfg.set_hr_upscaler(config["hr_upscaler"])
        if "hr_second_pass_steps" in config:
            image_cfg.set_hr_second_pass_steps(config["hr_second_pass_steps"])
        if "subseed" in config:
            image_cfg.set_subseed(config["subseed"])
        if "subseed_strength" in config:
            image_cfg.set_subseed_strength(config["subseed_strength"])
        if "seed_resize_from_h" in config:
            image_cfg.set_seed_resize_from_h(config["seed_resize_from_h"])
        if "seed_resize_from_w" in config:
            image_cfg.set_seed_resize_from_w(config["seed_resize_from_w"])
        if "hr_resize_x" in config:
            image_cfg.set_hr_resize_x(config["hr_resize_x"])
        if "hr_resize_y" in config:
            image_cfg.set_hr_resize_y(config["hr_resize_y"])
        if "styles" in config:
            image_cfg.set_styles(config["styles"])
        if "s_churn" in config:
            image_cfg.set_s_churn(config["s_churn"])
        if "s_tmax" in config:
            image_cfg.set_s_tmax(config["s_tmax"])
        if "s_tmin" in config:
            image_cfg.set_s_tmin(config["s_tmin"])
        if "s_noise" in config:
            image_cfg.set_s_noise(config["s_noise"])
        if "override_settings" in config:
            image_cfg.set_override_settings(config["override_settings"])
        if "override_settings_restore_afterwards" in config:
            image_cfg.set_override_settings_restore_afterwards(
                config["override_settings_restore_afterwards"]
            )
        if "script_args" in config:
            image_cfg.set_script_args(config["script_args"])
        if "sampler_index" in config:
            image_cfg.set_sampler_index(config["sampler_index"])
        if "script_name" in config:
            image_cfg.set_script_name(config["script_name"])
        if "send_images" in config:
            image_cfg.set_send_images(config["send_images"])
        if "save_images" in config:
            image_cfg.set_save_images(config["save_images"])
        if "alwayson_scripts" in config:
            image_cfg.set_alwayson_scripts(config["alwayson_scripts"])
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
            "seed": self.seed,
            "enable_hr": self.enable_hr,
            "denoising_strength": self.denoising_strength,
            "firstphase_width": self.firstphase_width,
            "firstphase_height": self.firstphase_height,
            "hr_scale": self.hr_scale,
            "hr_upscaler": self.hr_upscaler,
            "hr_second_pass_steps": self.hr_second_pass_steps,
            "hr_resize_x": self.hr_resize_x,
            "hr_resize_y": self.hr_resize_y,
            "styles": self.styles,
            "subseed": self.subseed,
            "subseed_strength": self.subseed_strength,
            "seed_resize_from_h": self.seed_resize_from_h,
            "seed_resize_from_w": self.seed_resize_from_w,
            "tiling": self.tiling,
            "do_not_save_samples": self.do_not_save_samples,
            "do_not_save_grid": self.do_not_save_grid,
            "restore_faces": self.restore_faces,
            "negative_prompt": self.negative_prompt,
            "eta": self.eta,
            "s_churn": self.s_churn,
            "s_tmax": self.s_tmax,
            "s_tmin": self.s_tmin,
            "s_noise": self.s_noise,
            "override_settings": self.override_settings,
            "override_settings_restore_afterwards": self.override_settings_restore_afterwards,
            "script_args": self.script_args,
            "sampler_index": self.sampler_index,
            "script_name": self.script_name,
            "send_images": self.send_images,
            "save_images": self.save_images,
            "alwayson_scripts": self.alwayson_scripts,
        }   
        return config
    


