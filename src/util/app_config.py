import yaml
from dataclasses import dataclass, field
import inspect


@dataclass
class AppConfig:
    # required feishu
    APP_ID: str
    APP_SECRET: str
    APP_ENCRYPT_KEY: str
    APP_VERIFICATION_TOKEN: str
    BOT_NAME: str
    # endrequired
    HTTP_PORT: int
    
    WEBUI_HOST: str
    WEBUI_PORT: int
    WEBUI_USE_HTTPS: bool
    WEBUI_USER: str
    WEBUI_PASSWORD: str

    ALIYUN_ACCESS_KEY_ID: str
    ALIYUN_ACCESS_KEY_SECRET: str
    ALIYUN_MT_REGION_ID: str
    
    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items() if k in inspect.signature(cls).parameters
        })

    def validate(self):
        if not self.APP_ID:
            raise Exception('APP_ID is required')
        if not self.APP_SECRET:
            raise Exception('APP_SECRET is required')
        if not self.APP_ENCRYPT_KEY:
            raise Exception('APP_ENCRYPT_KEY is required')
        if not self.APP_VERIFICATION_TOKEN:
            raise Exception('APP_VERIFICATION_TOKEN is required')
        if not self.BOT_NAME:
            raise Exception('BOT_NAME is required')
        if not self.HTTP_PORT:
            raise Exception('HTTP_PORT is required')

        if not self.WEBUI_HOST:
            raise Exception('WEBUI_HOST is required')
        if not self.WEBUI_PORT:
            raise Exception('WEBUI_PORT is required')
        # if not self.WEBUI_USE_HTTPS:
        #     raise Exception('WEBUI_USE_HTTPS is required')
        # if not self.WEBUI_USER:
        #     raise Exception('WEBUI_USER is required')
        # if not self.WEBUI_PASSWORD:
        #     raise Exception('WEBUI_PASSWORD is required')


def load_config():
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        appConfig = AppConfig.from_dict(config)
        appConfig.validate()
        return appConfig


app_config: AppConfig = load_config()

if __name__ == '__main__':
    load_config()
