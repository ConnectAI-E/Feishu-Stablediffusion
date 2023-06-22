<p align='center'>
古人云：道生一，一生二，二生StableDiffuion，StableDiffusion生万物
<a href='https://www.connectai-e.com' target="_blank" rel="noopener noreferrer">
<img width="1000" alt="image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/16874002/238823929-9c9233e5-6a3e-42e4-b562-760af22143ec.png">
</a>

<details align='center'>
<summary> 📷 点击展开完整功能截图 </summary>
<br>
<p align='center'>
<h1>Txt2Img：文生图</h1>
   <img width="1000" alt="image" src="https://github.com/ConnectAI-E/Feishu-Stablediffusion/assets/16874002/af5e0beb-dbf7-4f5a-b34c-1d9b0b6976cd">
    <img width="1000" alt="image" src="https://github.com/ConnectAI-E/Feishu-Stablediffusion/assets/16874002/374c8f91-3662-4aaf-8f57-c8decb8771ce">
<h1>Img2Txt：图生文</h1>
    <img width="1000" alt="image" src="https://github.com/ConnectAI-E/Feishu-Stablediffusion/assets/16874002/88922eb8-89f5-40e8-ab7f-42317296ba29">
<h1>Img2Img：图生图</h1>
    <img width="1000" alt="image" src="https://github.com/ConnectAI-E/Feishu-Stablediffusion/assets/16874002/d837171c-c872-425b-9625-4e3fef11c1e7">
</p>
</details>

---

</p>

<p align='center'>
   🎭 由stablediffusion赋能的飞书图片生成类机器人
<br>
<br>
    🚀 Feishu SD 🚀
</p>








## 功能点

- [X] txt2img: 通过正反词生成图片，支持**中英**双语
- [X] img2img: 支持以图生图
- [X] img2txt: 支持 clip 模型识别图片内容
- [X] 显示StableDiffusion服务器的相关信息
- [X] 可以选择 model
- [X] 可以设置生成图片的 size、step 与 seed 等参数
- [X] 显示图片生成信息
- [ ] ControlNet

---

## 部署 Stable Diffusion WebUI
> 项目使用[Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)作为后端(带 `--api`参数启动)，飞书作为前端，通过机器人，不再需要打开网页，在飞书里就可以使用StableDiffusion进行各种创作！
<details align='left'>
<summary> 📷 点击查看详细步骤 </summary>
<br>
   
### 更新 python 版本 

使用 pyenv 安装 Python 3.10.6

按以下命令依次执行

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
sudo apt install wget lzma liblzma-dev build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev 
pyenv install 3.10.6
pyenv global 3.10.6
```

### 切换国内 Linux 安装镜像

```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim/etc/apt/sources.list

# 修改为下列源内容
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse 
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse 
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse 
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse 
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse 
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse 
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse 
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse 
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse 
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
# 源结束结束


sudo apt-get update
sudo apt-get upgrade
```

### 安装 Nvidia 驱动

```
sudo apt update
sudo apt upgrade
sudo apt install nvidia-driver-530 nvidia-dkms-530
sudo reboot
```

等待重启，重新登录服务器，测试安装驱动成功
```
nvidia-smi
```


### 安装stable-diffusion-webui 并启动服务

```
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git ~/stable-diffusion-webui
cd ~/stable-diffusion-webui && bash webui.sh --api --listen
## 等待安装完成，运行成功后，Ctrl+C停止进程，然后运行下面命令后台运行 stable-diffusion-webui
cd ~/stable-diffusion-webui && nohup bash webui.sh --api --listen &
```

</details>

## 部署飞书机器人

1. 将*config-example.yml*复制为*config.yml*；
2. 编辑*config.yml*，添加机器人以及 StableDiffusionWebUI 的服务器信息；
3. （可选）创建 Python 虚拟环境 `python3 -m venv .venv && source .venv/bin/activate`；
4. 安装依赖库 `pip install -r requirements.txt`，然后运行 `python3 src/main.py`；
5. 其他飞书配置步骤，参考 [飞书-OpenAI](https://github.com/ConnectAI-E/Feishu-OpenAI) 部署指南 

## 操作方式

- 以/开头的为操作命令
  - eg: `/model`
- 只发文字消息为 txt2img，消息内容作为 prompt 和参数，通过#号分开正反词
  - eg: `1girl # lowres,bad anatomy,bad hands`
- 发图片带文字为 img2img，图片为基图，文字为 prompt 和参数
- 只发图片为 img2txt，返回图片识别的内容

## 操作命令

- 不带参数的：

| 命令            | 功能                                       |
| --------------- | ------------------------------------------ |
| /help           | 显示帮助                                   |
| /list_models    | 显示可用的模型                             |
| /list_sampler   | 显示可用的采样器                           |
| /list_upscalers | 显示可用的放大器                           |
| /host_info      | 显示最大内存，可用内存，最大显存，可用显存 |
| /quene          | 查询当前生成队列里的任务情况               |
| /model          | 显示当前模型                               |

- 带参数的：

| 命令   | 参数 | 功能                     |  |
| ------ | ---- | ------------------------ | - |
| /model | str  | 设置 StableDiffuion 模型 |  |

## 设置关键词:

- 使用关键词的格式--key [value]
  - eg: `--sampler [DPM++ 2S a Karras] --steps [30] --height [768]`
    (_bool 类型的不用带参数，写了就是 True_)

| 参数                 | 类型  | 功能                        | 默认值    |
| -------------------- | ----- | --------------------------- | --------- |
| --sampler            | str   | 设置采样器                  | "Euler a" |
| --steps              | int   | 设置采样步数                | 20        |
| --width              | int   | 设置宽度                    | 512       |
| --height             | int   | 设置高度                    | 512       |
| --batch_size         | int   | 设置批次大小                | 1         |
| --batch_count        | int   | 设置批次数量                | 1         |
| --seed               | int   | 设置种子                    | -1        |
| --cfg_scale          | float | 设置提示词的控制度          | 7.0       |
| --restore_faces      | bool  | 设置是否修复面容            | False     |
| --enable_hr          | bool  | 设置是否高清修复            | False     |
| --hr_upscaler        | str   | 设置放大器                  | Latent    |
| --hr_scale           | flat  | 设置放大倍率                | 2         |
| --denoising_strength | float | 设置重绘强度                | 0.7       |
| --resize_mode        | int   | 设置缩放模式                | 0         |

## 探索企联AI

| <div style="width:200px">AI</div> |             <img width=120> SDK <img width=120>              |                         Application                          |
| :-------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|              🎒OpenAI              |    [Go-OpenAI](https://github.com/ConnectAI-E/Go-OpenAI)     | [🏅Feishu-OpenAI](https://github.com/ConnectAI-E/Feishu-OpenAI), [🎖Lark-OpenAI](https://github.com/ConnectAI-E/Lark-OpenAI), [Feishu-EX-ChatGPT](https://github.com/ConnectAI-E/Feishu-EX-ChatGPT), [🎖Feishu-OpenAI-Stream-Chatbot](https://github.com/ConnectAI-E/Feishu-OpenAI-Stream-Chatbot), [Feishu-TLDR](https://github.com/ConnectAI-E/Feishu-TLDR),[Feishu-OpenAI-Amazing](https://github.com/ConnectAI-E/Feishu-OpenAI-Amazing), [Feishu-Oral-Friend](https://github.com/ConnectAI-E/Feishu-Oral-Friend), [Feishu-OpenAI-Base-Helper](https://github.com/ConnectAI-E/Feishu-OpenAI-Base-Helper), [Feishu-Vector-Knowledge-Management](https://github.com/ConnectAI-E/Feishu-Vector-Knowledge-Management), [Feishu-OpenAI-PDF-Helper](https://github.com/ConnectAI-E/Feishu-OpenAI-PDF-Helper), [🏅Dingtalk-OpenAI](https://github.com/ConnectAI-E/Dingtalk-OpenAI), [Wework-OpenAI](https://github.com/ConnectAI-E/Wework-OpenAI), [WeWork-OpenAI-Node](https://github.com/ConnectAI-E/WeWork-OpenAI-Node), [llmplugin](https://github.com/ConnectAI-E/llmplugin) |
|             🤖 AutoGPT             |                            ------                            | [🏅AutoGPT-Next-Web](https://github.com/ConnectAI-E/AutoGPT-Next-Web) |
|         🎭 Stablediffusion         |                            ------                            | [🎖Feishu-Stablediffusion](https://github.com/ConnectAI-E/Feishu-Stablediffusion) |
|           🍎 Midjourney            | [Go-Midjourney](https://github.com/ConnectAI-E/Go-Midjourney) | [🏅Feishu-Midjourney](https://github.com/ConnectAI-E/Feishu-Midjourney), [🔥MidJourney-Web](https://github.com/ConnectAI-E/MidJourney-Web), [Dingtalk-Midjourney](https://github.com/ConnectAI-E/Dingtalk-Midjourney) |
|            🍍 文心一言             |    [Go-Wenxin](https://github.com/ConnectAI-E/Go-Wenxin)     | [Feishu-Wenxin](https://github.com/ConnectAI-E/Feishu-Wenxin), [Dingtalk-Wenxin](https://github.com/ConnectAI-E/Dingtalk-Wenxin), [Wework-Wenxin](https://github.com/ConnectAI-E/Wework-Wenxin) |
|             💸 Minimax             |   [Go-Minimax](https://github.com/ConnectAI-E/Go-Minimax)    | [Feishu-Minimax](https://github.com/ConnectAI-E/Feishu-Minimax), [Dingtalk-Minimax](https://github.com/ConnectAI-E/Dingtalk-Minimax), [Wework-Minimax](https://github.com/ConnectAI-E/Wework-Minimax) |
|             ⛳️ CLAUDE              |    [Go-Claude](https://github.com/ConnectAI-E/Go-Claude)     | [Feishu-Claude](https://github.com/ConnectAI-E/Feishu-Claude), [DingTalk-Claude](https://github.com/ConnectAI-E/DingTalk-Claude), [Wework-Claude](https://github.com/ConnectAI-E/Wework-Claude) |
|              🥁 PaLM               |      [Go-PaLM](https://github.com/ConnectAI-E/go-PaLM)       | [Feishu-PaLM](https://github.com/ConnectAI-E/Feishu-PaLM),[DingTalk-PaLM](https://github.com/ConnectAI-E/DingTalk-PaLM),[Wework-PaLM](https://github.com/ConnectAI-E/Wework-PaLM) |
|             🎡 Prompt              |                            ------                            | [📖 Prompt-Engineering-Tutior](https://github.com/ConnectAI-E/Prompt-Engineering-Tutior) |
|             🍋 ChatGLM             |                            ------                            | [Feishu-ChatGLM](https://github.com/ConnectAI-E/Feishu-ChatGLM) |
|            ⛓ LangChain            |                            ------                            | [📖 LangChain-Tutior](https://github.com/ConnectAI-E/LangChain-Tutior) |
|            🪄 One-click            |                            ------                            | [🎖Awesome-One-Click-Deployment](https://github.com/ConnectAI-E/Awesome-One-Click-Deployment) |



