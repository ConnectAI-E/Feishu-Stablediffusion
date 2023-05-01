from util.app_config import app_config

COMMAND_CARD = {
  "elements": [
    {
      "tag": "div",
      "text": {
        "content": "命令列表",
        "tag": "plain_text"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "新的会话"
          },
          "type": "default",
          "value": {
            "action": "newchat"
          }
        }
      ]
    },
    {
      "tag": "hr"
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "select_static",
          "placeholder": {
            "tag": "plain_text",
            "content": "选择新的机器人预设"
          },
          "value": {
            "action": "prompt"
          },
          "options": [
            {
              "text": {
                "tag": "plain_text",
                "content": "AI助手（初始选项）"
              },
              "value": "default"
            }
          ],
          "confirm": {
            "title": {
              "tag": "plain_text",
              "content": "是否使用新的预设开始会话"
            },
            "text": {
              "tag": "plain_text",
              "content": "继续将清空当前会话"
            }
          }
        }
      ]
    },
    {
      "tag": "note",
      "elements": [
        {
          "tag": "plain_text",
          "content": "使用自定义预设：/prompt <你想要的预设>"
        }
      ]
    }
  ]
}