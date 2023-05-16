
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


- [x] txt2img: 通过正反prompt生成图片，通过#号分开正反词
- [x] img2img: 支持以图生图
- [x] img2txt: 支持clip模型识别图片内容
- [x] 可以选择model
- [x] 可以设置生成图片的size、step与seed等参数
- [x] 显示图片生成信息

后续看时间加入img2img, clip, controlnet等功能

## 飞书机器人基础环境搭建
1. 将config-example.yml复制为config.yml；
2. 编辑config.yml，添加机器人以及StableDiffusionWebUI的服务器信息；
3. （可选）创建Python虚拟环境python3 -m venv .venv && source .venv/bin/activate；
4. 安装依赖库pip install -r requirements.txt，然后运行python3 src/main.py；

## 操作方式

* 以/开头的为操作命令
* 只发文字消息为txt2img，消息内容作为prompt和参数
* 发图片带文字为img2img，图片为基图，文字为prompt和参数
* 只发图片为img2txt，返回图片识别的内容

## 操作命令
* 不带参数的：
1. /help 		显示帮助；
2. /list_models 	显示可用的模型；
3. /list_sampler 	显示可用的采样器;
4. /list_upscalers 	显示可用的放大器；
5. /host_info 		显示最大内存，可用内存，最大显存，可用显存；
6. /quene 		查询当前生成队列里的任务情况；
7. /model		显示当前模型

* 带参数的：
1. /model str 		设置StableDiffuion模型；

## 设置关键词，bool类型的不用带参数，写了就是True：
1. --sampler str 	设置采样器，默认"Euler a"；
2. --steps int 		设置采样步数，默认20；
3. --width int		设置宽度，默认512；
4. --height int 	设置高度，默认512；
5. --batch_size int	设置批次大小，默认为1；
6. --batch_count int 	设置批次数量，默认为1；
7. --seed int 		设置种子，默认为-1；
8. --cfg_scale float 	设置CFG大小，用来设置提示词的控制度，默认为7.0；
9. --restore_faces 	设置是否修复面容，默认为False；
10. --enable_hr 	设置是否高清修复，默认为False；
11. --hr_upscaler str 	设置放大器，默认为Latent；
12. --hr_scale flat 	设置放大倍率，默认为2；
13. --denoising_strength float	设置重绘强度，默认为0.7；
14. --resize_mode int 	设置缩放模式，默认为0；
15. --image_cfg_scale float 	设置Img2Img时原图的控制度；

