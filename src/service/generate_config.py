from webuiapi import HiResUpscaler, ControlNetUnit
from typing import List, Dict, Any
from feishu.message_card import LIST_INFO_CARD, handle_list_info_card
import translators as ts
import html

class GenerateConfig:
    def get_as_json(self) -> dict:
        return self.__dict__

    def update_from_json(self, json: dict):
        for key in json:
            if hasattr(self, key):
                setattr(self, key, json[key])
            else:
                print(f'Unknown key {key} in json')

    def translate_to_english(self):
        if len(self.prompt) > 0:
            self.prompt = ts.translate_text(query_text=self.prompt, translator='alibaba', from_language='auto', to_language='en')
        if len(self.negative_prompt) > 0:
            self.negative_prompt = ts.translate_text(query_text=self.negative_prompt, translator='alibaba', from_language='auto', to_language='en')


class TextToImageConfig(GenerateConfig):
    def __init__(
        self,
        enable_hr=False,
        denoising_strength=0.7,
        firstphase_width=0,
        firstphase_height=0,
        hr_scale=2,
        hr_upscaler=HiResUpscaler.Latent,
        hr_second_pass_steps=0,
        hr_resize_x=0,
        hr_resize_y=0,
        prompt="",
        styles=[],
        seed=-1,
        subseed=-1,
        subseed_strength=0.0,
        seed_resize_from_h=0,
        seed_resize_from_w=0,
        sampler_name=None,  # use this instead of sampler_index
        batch_size=1,
        n_iter=1,
        steps=None,
        cfg_scale=7.0,
        width=512,
        height=512,
        restore_faces=True,
        tiling=False,
        do_not_save_samples=False,
        do_not_save_grid=False,
        negative_prompt="",
        eta=1.0,
        s_churn=0,
        s_tmax=0,
        s_tmin=0,
        s_noise=1,
        override_settings={},
        override_settings_restore_afterwards=True,
        script_args=None,  # List of arguments for the script "script_name"
        script_name=None,
        send_images=True,
        save_images=False,
        alwayson_scripts={},
        controlnet_units: List[ControlNetUnit] = [],
        sampler_index=None,  # deprecated: use sampler_name
        use_deprecated_controlnet=False,
    ):
        self.enable_hr = enable_hr
        self.denoising_strength = denoising_strength
        self.firstphase_width = firstphase_width
        self.firstphase_height = firstphase_height
        self.hr_scale = hr_scale
        self.hr_upscaler = hr_upscaler
        self.hr_second_pass_steps = hr_second_pass_steps
        self.hr_resize_x = hr_resize_x
        self.hr_resize_y = hr_resize_y
        self.prompt = prompt
        self.styles = styles
        self.seed = seed
        self.subseed = subseed
        self.subseed_strength = subseed_strength
        self.seed_resize_from_h = seed_resize_from_h
        self.seed_resize_from_w = seed_resize_from_w
        self.sampler_name = sampler_name
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.restore_faces = restore_faces
        self.tiling = tiling
        self.do_not_save_samples = do_not_save_samples
        self.do_not_save_grid = do_not_save_grid
        self.negative_prompt = negative_prompt
        self.eta = eta
        self.s_churn = s_churn
        self.s_tmax = s_tmax
        self.s_tmin = s_tmin
        self.s_noise = s_noise
        self.override_settings = override_settings
        self.override_settings_restore_afterwards = override_settings_restore_afterwards
        self.script_args = script_args
        self.script_name = script_name
        self.send_images = send_images
        self.save_images = save_images
        self.alwayson_scripts = alwayson_scripts
        self.controlnet_units = controlnet_units
        self.sampler_index = sampler_index
        self.use_deprecated_controlnet = use_deprecated_controlnet


class ImageToImageConfig(GenerateConfig):
    def __init__(
        self,
        images=[],  # list of PIL Image
        resize_mode=0,
        denoising_strength=0.75,
        image_cfg_scale=1.5,
        mask_image=None,  # PIL Image mask
        mask_blur=4,
        inpainting_fill=0,
        inpaint_full_res=True,
        inpaint_full_res_padding=0,
        inpainting_mask_invert=0,
        initial_noise_multiplier=1,
        prompt="",
        styles=[],
        seed=-1,
        subseed=-1,
        subseed_strength=0,
        seed_resize_from_h=0,
        seed_resize_from_w=0,
        sampler_name=None,  # use this instead of sampler_index
        batch_size=1,
        n_iter=1,
        steps=None,
        cfg_scale=7.0,
        width=512,
        height=512,
        restore_faces=True,
        tiling=False,
        do_not_save_samples=False,
        do_not_save_grid=False,
        negative_prompt="",
        eta=1.0,
        s_churn=0,
        s_tmax=0,
        s_tmin=0,
        s_noise=1,
        override_settings={},
        override_settings_restore_afterwards=True,
        script_args=None,  # List of arguments for the script "script_name"
        sampler_index=None,  # deprecated: use sampler_name
        include_init_images=False,
        script_name=None,
        send_images=True,
        save_images=False,
        alwayson_scripts={},
        controlnet_units: List[ControlNetUnit] = [],
        use_deprecated_controlnet=False,
    ):
        self.images = images
        self.resize_mode = resize_mode
        self.denoising_strength = denoising_strength
        self.image_cfg_scale = image_cfg_scale
        self.mask_image = mask_image
        self.mask_blur = mask_blur
        self.inpainting_fill = inpainting_fill
        self.inpaint_full_res = inpaint_full_res
        self.inpaint_full_res_padding = inpaint_full_res_padding
        self.inpainting_mask_invert = inpainting_mask_invert
        self.initial_noise_multiplier = initial_noise_multiplier
        self.prompt = prompt
        self.styles = styles
        self.seed = seed
        self.subseed = subseed
        self.subseed_strength = subseed_strength
        self.seed_resize_from_h = seed_resize_from_h
        self.seed_resize_from_w = seed_resize_from_w
        self.sampler_name = sampler_name
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.restore_faces = restore_faces
        self.tiling = tiling
        self.do_not_save_samples = do_not_save_samples
        self.do_not_save_grid = do_not_save_grid
        self.negative_prompt = negative_prompt
        self.eta = eta
        self.s_churn = s_churn
        self.s_tmax = s_tmax
        self.s_tmin = s_tmin
        self.s_noise = s_noise
        self.override_settings = override_settings
        self.override_settings_restore_afterwards = override_settings_restore_afterwards
        self.script_args = script_args
        self.sampler_index = sampler_index
        self.include_init_images = include_init_images
        self.script_name = script_name
        self.send_images = send_images
        self.save_images = save_images
        self.alwayson_scripts = alwayson_scripts
        self.controlnet_units = controlnet_units
        self.use_deprecated_controlnet = use_deprecated_controlnet
