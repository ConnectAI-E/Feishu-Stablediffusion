# -*- coding: utf-8 -*-
from util.app_config import app_config

from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class AliyunTranslator:
    def __init__(self):
        config = open_api_models.Config(access_key_id=app_config.ALIYUN_ACCESS_KEY_ID, access_key_secret=app_config.ALIYUN_ACCESS_KEY_SECRET)
        config.endpoint = f'mt.{app_config.ALIYUN_MT_REGION_ID}.aliyuncs.com'
        self.client = alimt20181012Client(config)

    def translate(self, source_text, format_type='text', source_language='zh', target_language='en', scene='general'):
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            source_text=source_text, format_type=format_type, source_language=source_language, target_language=target_language, scene=scene
        )
        runtime = util_models.RuntimeOptions()
        try:
            result = self.client.translate_general_with_options(translate_general_request, runtime)
        except Exception as error:
            UtilClient.assert_as_string(error.message)

        return result.body.data.translated


aliyun_translator = AliyunTranslator()


def test_translate():
    print(aliyun_translator.translate('一个小女孩正在画画 <lora:add_detail:1>'))


if __name__ == '__main__':
    test_translate()
