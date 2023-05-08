import json
from util.app_config import app_config
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent

# bot need to be mentioned in first place
def is_mention_bot(event: MessageReceiveEvent) -> bool:
    mentions = event.event.message.mentions
    if event.event.message.mentions is None or mentions[0].name != app_config.BOT_NAME:
        return False

    return True

def get_mention_message(event: MessageReceiveEvent) -> str:
    if is_mention_bot(event):
        content = json.loads(event.event.message.content)
        if "text" in content:
            text = content["text"]
            return text.split(" ", 1)[1]
        
    return None

def get_pure_message(event: MessageReceiveEvent) -> str:
    if event.event.message.chat_type == "group":
        return get_mention_message(event)
    else:
        return json.loads(event.event.message.content)['text']