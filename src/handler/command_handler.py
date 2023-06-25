import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import message_sender
from util.logger import app_logger
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent


class CommandHandler:
    def __init__(self):
        pass

    def handle_command(self, myevent: MyReceiveEvent):
        command = myevent.get_command()

        if command == 'help':
            # message_sender.send_text_message(myevent, sd_webui.help())
            message_sender.send_message_card(myevent,sd_webui.helpCard())
            app_logger.info(f"command /help")
        elif command == 'list_models':
            message_sender.send_text_message(myevent, sd_webui.list_models())
            app_logger.info(f"command /list_models")
        elif command == 'list_samplers':
            message_sender.send_text_message(myevent, sd_webui.list_samplers())
            app_logger.info(f"command /list_samplers")
        elif command == 'list_upscalers':
            message_sender.send_text_message(myevent, sd_webui.list_upscalers())
            app_logger.info(f"command /list_upscalers")
        elif command == 'list_controlnet_modules':
            message_sender.send_text_message(myevent, sd_webui.list_controlnet_modules())
            app_logger.info(f"command /list_controlnet_modules")
        elif command == 'list_controlnet_models':
            message_sender.send_text_message(myevent, sd_webui.list_controlnet_models())
            app_logger.info(f"command /list_controlnet_models")
        elif command == 'refresh_models':
            sd_webui.refresh_models()
            message_sender.send_text_message(myevent, '模型列表已刷新')
            app_logger.info(f"command /refresh_models")
        elif command == 'host_info':
            message_sender.send_text_message(myevent, sd_webui.host_info())
            app_logger.info(f"command /host_info")
        elif command == 'queue':
            message_sender.send_text_message(myevent, sd_webui.queue())
            app_logger.info(f"command /queue")
        elif command == 'model':
            model = myevent.get_command_args()
            if model is None:
                model = sd_webui.get_model()
                message_sender.send_text_message(myevent, f'当前模型为: [{model}]')
            else:
                sd_webui.set_model(model)
                message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        else:
            message_sender.send_text_message(myevent, "未知命令，请使用 /help 查看帮助")
            app_logger.info("unknown command")
            
        return True
