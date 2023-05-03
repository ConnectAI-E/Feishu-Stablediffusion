import os
from larksuiteoapi import Config, DOMAIN_FEISHU, LEVEL_INFO
from util.app_config import app_config

os.environ["APP_ID"] = app_config.APP_ID
os.environ["APP_SECRET"] = app_config.APP_SECRET
os.environ["ENCRYPT_KEY"] = app_config.APP_ENCRYPT_KEY
os.environ["VERIFICATION_TOKEN"] = app_config.APP_VERIFICATION_TOKEN
os.environ["BOT_NAME"] = app_config.BOT_NAME

# for Cutome APP（企业自建应用）
app_settings = Config.new_internal_app_settings_from_env()
# for memory store and logger(level=debug)
feishu_conf = Config(DOMAIN_FEISHU, app_settings, log_level=LEVEL_INFO)
