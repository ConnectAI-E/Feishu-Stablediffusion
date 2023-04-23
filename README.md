# Feishu-Stablediffusion
🎭 由stablediffusion赋能的飞书图片生成类机器人

## Refer

-  [Hugging Face](https://huggingface.co/runwayml/stable-diffusion-v1-5)

```sh
curl https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5 \
	-X POST \
	-d '{"inputs": "Astronaut riding a horse"}' \
	-H "Authorization: Bearer api_org_xxxxxx"
```

- [ ] 通过正反prompt生成图片
- [ ] 可以选择model（常用风格代表）
- [ ] 可以设置生成图片的size、step与seed
- [ ] 每张图片自带基本生成信息

后续看时间加入img2img, clip, controlnet等功能

## 飞书机器人基础环境搭建


- copy the config-example.yml to config.yml
- edit config.yml to your needs
- (optional) create python virtual environment python3 -m venv .venv && source .venv/bin/activate
- install requirements pip install -r requirements.txt
- run python3 src/main.py


