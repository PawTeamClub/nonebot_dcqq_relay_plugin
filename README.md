<p align="center">
  <img src="https://raw.githubusercontent.com/PawTeamClub/.github/main/paw_temporary_icons.png" width="200" height="200">
</p>

<div align="center">
  
# nonebot_dcqq_relay_plugin

<br />

_✨ 使用Nonebot2让Discord和QQ群实现互相通信 ✨_

<img src="https://img.shields.io/badge/OneBot-11-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="Badge"> <img src="https://img.shields.io/badge/logo-Discord-5865F2.svg?logo=discord" alt="Badge">

</div>

# 介绍

使用Onebot V11适配器和Discord适配器来实现对Discord与QQ群互相交流的插件。

理论支持所有使用Onebot V11的框架, 只不过有些框架可能会遇到问题，请自行测试。

目前只支持普通的文字频道，不支持帖子频道 (也不打算支持)

[如果你嫌这个项目不够好用，可以尝试Autuamn大大的nonebot-plugin-dcqq-relay插件](https://github.com/Autuamn/nonebot-plugin-dcqq-relay)

# 功能

**ARK消息和Embed消息暂不打算支持**

### 目前支持的消息：
- [x] 文字
- [x] 图片
- [x] 表情 (表情超市或QQ默认表情(除了高级表情)基本都支持)
- [x] 回复消息
- [x] 文件 
- [x] 撤回消息 ([如果你使用的是Lagrange.Onebot那么可能会失效](#已知BUG列表))

### 尚未支持的消息：
- [ ] 语音
- [ ] 视频

# 安装

目前此插件还在早期开发阶段，还有许多问题，如果遇到问题还请务必提 [issue](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/issues)。

<details>
<summary>使用包管理器安装（推荐）</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-dcqq-relay-plugin
</details>
<details>
<summary>pdm (未测试)</summary>

    pdm add nonebot-dcqq-relay-plugin
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-dcqq-relay-plugin
</details>


打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin('nonebot_dcqq_relay_plugin')

</details>

<details>
<summary>从 github 安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 输入以下命令克隆此储存库

    git clone https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin.git
  
打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin('src.plugins.nonebot_dcqq_relay_plugin')

</details>

# 配置

## DISCORD_CHANNEL

**你需要开启Discord的开发者模式获取频道ID**

填写需要转发的Discord频道ID

[如果你不知道怎么开启开发者模式，点我](https://beebom.com/how-enable-disable-developer-mode-discord/#:~:text=Turn%20on%20Discord%20Developer%20Mode%20%28Android%2C%20iOS%29%201,access%20the%20IDs%20of%20channels%20and%20messages.%20)

```json
DISCORD_CHANNEL="1234567890000000000000"
```

## ONEBOT_CHANNEL

填写需要转发的QQ群号

```json
ONEBOT_CHANNEL="123456789"
```

## DATA_DIR (未测试)

修改数据文件默认存储路径，默认存在包安装目录下

```json
DATA_DIR="./data/"
```

## env配置例子

```
# nonebot2默认配置
DRIVER=~fastapi+~httpx+~websockets

# nonebot_dcqq_relay_plugin配置
DISCORD_CHANNEL="1234567890000000000000"
ONEBOT_CHANNEL="123456789"

# nonebot2 discord适配器设置
DISCORD_PROXY='http://127.0.0.1:8080'
DISCORD_BOTS='
[
  {
    "token": "xxxxx",
    "intent": {
      "guild_messages": true,
      "guild_message_reactions": true,
      "direct_messages": true,
      "direct_message_reactions": true,
      "message_content": true
    },
    "application_commands": {"*": ["*"]}
  }
]
'
```

# Q & A

Q1: 遇到"unable to verify the first certificate"报错 (通常是因为使用了类似于steamcommunity 302反代工具和NapCatQQ框架的下载文件强制使用可信证书导致)

A1: 1. 强制修改源码 2. 使用代理工具全局代理，不要使用反代工具

Q2: 撤回无法使用

A2: 看[已知BUG列表第一条](#已知BUG列表)

Q3: 为何不做多QQ群多频道转发

A3: 技术力不够~~因为懒~~

# 已知BUG列表

1. Discord撤回onebot消息异常 (Lagrange.Onebot|Lagrange.Core的bug)
     - 问题: delete_smg函数总是撤回消息的id和接收消息的id不一样 (在[Lagrange.Core/issues#226](https://github.com/LagrangeDev/Lagrange.Core/issues/226#issuecomment-2009693106)的回答中也遇到了这个问题，暂时没有解决方案 ~~我也不会C#~~)
     - 为什么不给Lagrange团队丢issue: 虽然issue那边是Core的问题，但因为是相同问题所以我就不发了 ~~根本原因还是害怕挨骂和害怕交流~~
     - 使用LLOneBot、NapCatQQ框架测试时没有问题
2. 当一个人发了多图多文或者是多个表情的时候，可能会因为网络问题导致发送变慢

# TODO:
~~做几把@，做不了一点~~

# 感谢

- [nonebot/nonebot2](https://github.com/nonebot/nonebot2): 跨平台 Python 异步聊天机器人框架
- [koishijs/koishi-plugin-dcqq-relay](https://github.com/koishijs/koishi-plugin-dcqq-relay): 使用koishi实现同步Discord与QQ间的消息
- [Autuamn/nonebot-plugin-dcqg-relay](https://github.com/Autuamn/nonebot-plugin-dcqg-relay): 在QQ频道与 Discord 之间同步消息的 nonebot2 插件 [(抄了初始化的部分)](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/blob/main/nonebot_dcqq_relay_plugin/setup.py)