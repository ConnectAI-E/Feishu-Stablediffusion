import json
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent
from larksuiteoapi import Config, Context
from typing import Any
from message_router import message_handler
import threading

def action_im_message(ctx: Context, conf: Config, card: MessageReceiveEvent) -> Any:
    if hasattr(card, 'action'):
        t = threading.Thread(target=handledelayedUpdateMessageCard(card.token, card.open_id, card.action.value["prompt"]))
        t.start()
    return {}

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

    