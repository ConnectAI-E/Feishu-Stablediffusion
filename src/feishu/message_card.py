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
    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": "根据如下参数生成:"}},
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": image_info.replace('\\', '')},
        },
    ]
    for img_key in img_key_list:
        elements.append(
            {
                "alt": {"content": "", "tag": "plain_text"},
                "img_key": img_key,
                "tag": "img",
            }
        )

    return {"config": {"wide_screen_mode": True}, "elements": elements}
