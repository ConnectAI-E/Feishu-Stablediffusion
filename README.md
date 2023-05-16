
<p align='center'>

  <img width="1000" alt="image" src="https://user-images.githubusercontent.com/50035229/236652971-3b37e644-7f29-4861-8a51-8445e4e588d3.png">
	
<details align='center'>
    <summary> 📷 点击展开完整功能截图</summary>
    <br>
    <p align='center'>
   <img width="1122" alt="image" src="https://user-images.githubusercontent.com/50035229/236653023-8cd147c6-c1de-44f1-a91f-6d8e2ce86f37.png">
   <img width="1120" alt="image" src="https://user-images.githubusercontent.com/50035229/236653053-f12d0208-2b03-40b2-a2e6-569c976014d8.png">
    </p>

</details>	
	
	
</p>

<p align='center'>
   🎭 由stablediffusion赋能的飞书图片生成类机器人
<br>
<br>
    🚀 Feishu SD 🚀
</p>

<p align='center'>
  😀Connect-AI-E开源马拉松正式开始评审环节啦😀
</p>

<p align='center'>
  快来pick你最喜欢的开源项目吧!
</p>
  
<p align='center'>
   https://wenjuan.feishu.cn/m/cfm?t=s6hfGkEr4pMi-8ph5
</p>


## Refer

- [Hugging Face](https://huggingface.co/runwayml/stable-diffusion-v1-5)

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

## 操作方式（开发中）

* 直接发消息就是做为提示词出图，其它参数都用会话绑定的状态数据。
* **显示信息类的命令：**

1. /help 显示帮助；
2. /list_models 显示可用的模型；
3. /list_sampler 显示可用的采样器;
4. /host_info 显示操作系统，CPU型号，最大内存，可用内存，GPU型号，最大显存，可用显存；
5. /quene 查询当前生成队列里的工作数；
6. /log n 显示最后n条日志，n不写默认为5；

* **设置状态类的命令，不带参数为显示当前状态参数。同时也可以把“/”换成“--”作为prompt中的参数，单次使用：**

1. /model 设置SD模型；
2. /negative 设置负提示词；
3. /sampler 设置采样器，默认"Euler a"；
4. /steps 设置采样步数，默认20；
5. /width 设置宽度，默认512；
6. /height 设置高度，默认512；
7. /batch_count 设置几个批次，默认为1；
8. /batch_size 设置单个批次的size，默认为1；
9. /cfg 设置cfg scale控制prompt的强度，默认为7；
10. /seed 设置生成用的种子，默认为-1；
