import json
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from handler.command_handler import CommandHandler
from handler.message_handler import MessageHandler
from util.app_config import app_config
from feishu.feishu_conf import feishu_conf
import threading

message_handler = MessageHandler(app_config, feishu_conf)
command_handler = CommandHandler(app_config, feishu_conf)

def action_im_message(ctx: Context, conf: Config, card: MessageReceiveEvent) -> Any:
    return card

def handledelayedUpdateMessageCard(token,openId, prompt):
    message_handler.handle_update_message_card(token, openId, prompt)

def delayedUpdateMessageCard(card):
    if card.action:
        t = threading.Thread(target=handledelayedUpdateMessageCard(card.token, card.open_id, card.action.value["prompt"]))
        t.start()
        return ""
    else:
        return json.dumps({
          "config": {
            "wide_screen_mode": True
          },
          "elements": [
            {
              "tag": "div",
              "text": {
                "content": "这是一段普通文本",
                "tag": "plain_text"
              }
            }
          ]
        })

    