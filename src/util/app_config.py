import yaml
from dataclasses import dataclass, field
import inspect


@dataclass
class AppConfig:
    # required
    APP_ID: str
    APP_SECRET: str
    APP_ENCRYPT_KEY: str
    APP_VERIFICATION_TOKEN: str
    BOT_NAME: str
    # endrequired
    # required if IS_AZURE is False
    OPENAI_KEY: str
    # endrequired if IS_AZURE is False
    IS_AZURE: bool
    # required if IS_AZURE is True
    AZURE_API_HOST: str
    AZURE_API_KEY: str
    GPT_MODEL: str
    # endrequired if IS_AZURE is True
    HTTP_PORT: int
    API_URL: str
    HTTP_PROXY: str
    DEFAULT_PROMPT: str
    PROMPT_DESCRIPTION_LIST: list
    PROMPT_VALUE_LIST: list

    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k: v for k, v in env.items() if k in inspect.signature(cls).parameters
        })

    def validate(self):
        if self.IS_AZURE:
            if not self.AZURE_API_HOST:
                raise Exception('AZURE_API_HOST is required when IS_AZURE is True')
            if not self.AZURE_API_KEY:
                raise Exception('AZURE_API_KEY is required when IS_AZURE is True')
            if not self.GPT_MODEL:
                raise Exception('GPT_MODEL is required when IS_AZURE is True')
        else:
            if not self.OPENAI_KEY:
                raise Exception('OPENAI_KEY is required when IS_AZURE is False')

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
        if not self.API_URL:
            raise Exception('API_URL is required')
        if not self.DEFAULT_PROMPT:
            raise Exception('DEFAULT_PROMPT is required')

        # PROMPT_DESCRIPTION_LIST and PROMPT_VALUE_LIST must have the same length
        if len(self.PROMPT_DESCRIPTION_LIST) != len(self.PROMPT_VALUE_LIST):
            raise Exception('PROMPT_DESCRIPTION_LIST and PROMPT_VALUE_LIST must have the same length')

def load_config():
    with open('config.yml', 'r',encoding='utf-8') as f:
        config = yaml.safe_load(f)
        appConfig = AppConfig.from_dict(config)
        appConfig.validate()
        return appConfig

app_config:AppConfig = load_config()

if __name__ == '__main__':
    load_config()
    
