import json
import attr
from util.app_config import app_config
from larksuiteoapi.service.im.v1.event import MessageReceiveEvent


class MyReceiveEvent:
    def __init__(self, event: MessageReceiveEvent) -> None:
        self.event = event
        event.message.content = json.loads(event.message.content)
        self.event_json = attr.asdict(event)
        self.text = None
        self.image_key = None
        self.audio_key = None
        self.media_key = None

        if self.get_message_type() == 'text':
            self.text = self.event.message.content['text']
            if self.is_group_chat() and self.is_mentioned_bot():
                texts = self.text.split(' ', 1)
                if len(texts) == 2:
                    self.text = texts[1].strip()
        elif self.get_message_type() == 'image':
            self.image_key = self.event.message.content['image_key']
        elif self.get_message_type() == 'audio':
            self.audio_key = self.event.message.content['file_key']
            self.audio_duration = self.event.message.content['duration']
        elif self.get_message_type() == 'media':
            self.media_key = self.event.message.content['file_key']
            self.media_image_key = self.event.message.content['image_key']
            self.media_file_name = self.event.message.content['file_name']
            self.media_duration = self.event.message.content['duration']
        elif self.get_message_type() == 'post':
            self.post_title = self.event.message.content['title']
            post_content = self.event.message.content['content']
            for item in post_content:
                for tag in item:
                    if tag['tag'] == 'text':
                        text = tag['text'].strip()
                        if len(text) > 0:
                            self.text = text
                    elif tag['tag'] == 'img':
                        self.image_key = tag['image_key']
                        self.image_width = tag['width']
                        self.image_height = tag['height']
                    elif tag['tag'] == 'media':
                        self.media_key = tag['file_key']
                        self.media_image_key = tag['image_key']

    def has_content(self) -> bool:
        return self.text is not None or self.image_key is not None or self.audio_key is not None or self.media_key is not None

    def is_mentioned(self, name: str) -> bool:
        if self.event.message.mentions is None:
            return False

        for mention in self.event.message.mentions:
            if mention.name == name:
                return True

        return False

    def is_mentioned_bot(self) -> bool:
        return self.is_mentioned(app_config.BOT_NAME)

    def is_group_chat(self) -> bool:
        return self.get_chat_type() == 'group'

    def is_command_msg(self) -> bool:
        if self.text is None:
            return False

        return self.text.startswith('/')

    def get_command(self) -> str:
        if not self.is_command_msg():
            return None

        command = self.text.split(' ', 1)[0]

        return command[1:].lower()

    def get_command_args(self) -> str:
        if not self.is_command_msg():
            return None

        command_args = self.text.split(' ', 1)
        if len(command_args) > 1:
            return command_args[1].strip()

        return None

    def get_event_json(self) -> dict:
        return self.event_json

    def get_chat_type(self) -> str:
        return self.event.message.chat_type

    def get_chat_id(self) -> str:
        return self.event.message.chat_id

    def get_message_type(self) -> str:
        return self.event.message.message_type

    def get_message_id(self) -> str:
        return self.event.message.message_id

    def get_sender_type(self) -> str:
        return self.event.sender.sender_type

    def get_user_id(self) -> str:
        return self.event.sender.sender_id.user_id

    def get_open_id(self) -> str:
        return self.event.sender.sender_id.open_id

    def get_union_id(self) -> str:
        return self.event.sender.sender_id.union_id
    
    def get_tenant_key(self) -> str:
        return self.event.sender.tenant_key
