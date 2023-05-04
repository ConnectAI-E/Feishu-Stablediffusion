import json

LIST_INFO_CARD = {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "根据的描述得到如下结果:"
                        }
                    }
                ]
            }

def handle_list_info_card(LIST_INFO_CARD, list):
    # Clear the existing elements array
    LIST_INFO_CARD["elements"] = []
    # Iterate through the input list and add an object to the elements array for each string
    for item in list:
        # Construct a new object with a "content" field set to the current string
        element = {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": item
            }
        }
        
        # Add the new object to the elements array
        LIST_INFO_CARD["elements"].append(element)
    # Return the updated LIST_INFO_CARD dictionary
    return LIST_INFO_CARD

def handle_image_card(image_cfg, img_key = 'img_v2_041b28e3-5680-48c2-9af2-497ace79333g'): 

    return {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "根据的描述得到如下结果:"
                        }
                    },
                    {
                        "alt": {
                            "content": "",
                            "tag": "plain_text"
                        },
                        "img_key": img_key,
                        "tag": "img"
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "你的参数配置如下:"
                        }
                    },
                {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": json.dumps(image_cfg)
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "帮助参数指令如下:"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": "/help 显示帮助；/list_models 显示可用的模型；/list_sampler 显示可用的采样器;/host_info 显示操作系统，CPU型号，最大内存，可用内存，GPU型号，最大显存，可用显存；/quene 查询当前生成队列里的工作数；/log n 显示最后n条日志，n不写默认为5；"
                        }
                    }
                ]
            }
        