import json

LIST_INFO_CARD = {
    "config": {"wide_screen_mode": True},
    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "根据的描述得到如下结果:"}}],
}

str_arr = [
    "variant",
    "scale",
    "Face restoration",
    "Size",
    "Model hash",
    "Model",
    "Seed resize from",
    "Denoising strength",
    "Clip skip",
    "Steps",
    "Sampler",
    "Seed",
    "Negative prompt",
    "prompt",
]

def handle_list_info_card(LIST_INFO_CARD, list):
    LIST_INFO_CARD["elements"] = []
    for item in list:
        element = {
            "tag": "div",
            "text": {"tag": "lark_md", "content": json.dumps(item)},
        }
        LIST_INFO_CARD["elements"].append(element)
    return LIST_INFO_CARD

def format_input_str(input_str, str_arr):
    for key in str_arr:
        input_str = input_str.replace(key + ':', '\n **【' + key + '】** ')
    return input_str

def handle_image_card(image_info, img_key_list, prompt):
    split_datas = []
    datas = json.loads(image_info)
    for data in datas['infotexts']:
      split_datas.append('prompt: '+ data.replace('\n', ''))

    elements = [
        {"tag": "column_set", "flex_mode": "none", "background_style": "default", "columns": []},
    ]

    for index, img_key in enumerate(img_key_list):
        print(split_datas[index])
        elements.append(
          {
                      "tag": "img",
                      "img_key": img_key,
                      "alt": {
                        "tag": "plain_text",
                        "content": ""
                      },
                      "mode": "fit_horizontal",
                      "preview": True
            })
        elements.append(
            {
                  "tag": "markdown",
                  "content": format_input_str(split_datas[index], str_arr),
            }
        )

    elements.append({
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
              "prompt": prompt,
            }
          }
        ]
    })
    return {"config": {"wide_screen_mode": True}, "elements": elements,  "header": {
      "template": "green",
      "title": {
        "content": "🤖️ 根据如下参数生成:",
        "tag": "plain_text"
      }
    }}
