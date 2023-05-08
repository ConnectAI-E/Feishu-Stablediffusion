import json

LIST_INFO_CARD = {
    "config": {"wide_screen_mode": True},
    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "根据的描述得到如下结果:"}}],
}


def handle_list_info_card(LIST_INFO_CARD, list):
    # Clear the existing elements array
    LIST_INFO_CARD["elements"] = []
    # Iterate through the input list and add an object to the elements array for each string
    for item in list:
        # Construct a new object with a "content" field set to the current string
        element = {
            "tag": "div",
            "text": {"tag": "lark_md", "content": json.dumps(item)},
        }

        # Add the new object to the elements array
        LIST_INFO_CARD["elements"].append(element)
    # Return the updated LIST_INFO_CARD dictionary
    return LIST_INFO_CARD


def handle_image_card(image_info, img_key_list):

    # 过滤字段 = ['all_prompts', 'infotexts']
    data = json.loads(image_info)
    filter_keys = ['all_prompts']
    new_data = {k: v for k, v in data.items() if k not in filter_keys}
    json_str = '\n'.join(' **【' + k + '】** ' + str(v) for k, v in new_data.items())

    elements = [
        {"tag": "column_set", "flex_mode": "none", "background_style": "default", "columns": []},
        {
        "tag": "markdown",
        "content": json_str
        },
        {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "重新生成"
            },
            "type": "primary",
            "value": {
              "type": "reload",
              "prompt": data['prompt'],
            }
          }
        ]
    }
    ]
    for img_key in img_key_list:
        elements[0]["columns"].append(
          {
          "tag": "column",
          "width": "weighted",
          "weight": 1,
          "vertical_align": "top",
          "elements": [
            {
              "tag": "column_set",
              "flex_mode": "none",
              "background_style": "grey",
              "columns": [
                {
                  "tag": "column",
                  "width": "weighted",
                  "weight": 1,
                  "vertical_align": "top",
                  "elements": [
                    {
                      "tag": "img",
                      "img_key": img_key,
                      "alt": {
                        "tag": "plain_text",
                        "content": ""
                      },
                      "mode": "fit_horizontal",
                      "preview": True
                    }
                  ]
                }
              ]
            }
          ]
        }
        )

    return {"config": {"wide_screen_mode": True}, "elements": elements,  "header": {
      "template": "green",
      "title": {
        "content": "🤖️ 根据如下参数生成:",
        "tag": "plain_text"
      }
    }}
