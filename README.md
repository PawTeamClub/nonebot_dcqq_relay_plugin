<p align="center">
  <img src="https://raw.githubusercontent.com/PawTeamClub/.github/main/paw_temporary_icons.png" width="200" height="200">
</p>

<div align="center">
  
# nonebot_dcqq_relay_plugin

<br />

_✨ 使用Nonebot2让Discord和QQ群实现互相通信 ✨_

<img src="https://img.shields.io/badge/OneBot-11-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="Badge"> <img src="https://img.shields.io/badge/logo-Discord-5865F2.svg?logo=discord" alt="Badge">

| [介绍](#介绍) - [支援功能](#功能) - [安装](#安装) - [感谢](#感谢)|
:----------------------------------------------------------: |
| [Q&A](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/wiki/Q&A) - [BUG列表](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/wiki/Bug-list) - [(务必查看) env配置](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/wiki/Config) - [TODO](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/wiki/TODO)|

</div>

# 介绍

使用Onebot V11适配器和Discord适配器来实现对Discord与QQ群互相交流的插件。

**理论支持所有使用Onebot V11的框架, 只不过有些框架可能会遇到问题，请自行测试。**

目前只支持普通的文字频道，不支持帖子频道 (也不打算支持)

语音频道也许后面会支持，但看看有没有这个需求。

[如果你嫌这个项目不够好用，可以尝试Autuamn大大的nonebot-plugin-dcqq-relay插件!!!](https://github.com/Autuamn/nonebot-plugin-dcqq-relay)

[如果你寻找的是discord和qq频道互相通信，请使用Autuamn大大的nonebot-plugin-dcqg-relay插件!!!](https://github.com/Autuamn/nonebot-plugin-dcqg-relay)

# 功能

**ARK消息和Embed消息暂不打算支持**

### 目前支持的消息：
- [x] 文字
- [x] 图片
- [x] 表情 (表情超市或QQ默认表情(除了高级表情)基本都支持)
- [x] 回复消息
- [x] 文件 
- [x] 撤回消息 ([如果你使用的是Lagrange.Onebot那么可能会失效](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/wiki/Bug-list))

### 尚未支持的消息：
- [ ] 语音
- [ ] 视频

# 安装

目前此插件还在早期开发阶段，还有许多问题！！！

然后这是我的python初作品(此前没写过任何一个python语言的东西)，所以可能代码层面不太理想，请见谅。 :(

如果遇到问题还请务必提 [issue](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/issues)。

---

<details>
<summary>使用包管理器安装（目前推荐）</summary>
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

如果你没有`bot.py`文件，请使用`nb-cli`生成bot文件

    nonebot.load_plugin('nonebot_dcqq_relay_plugin')

</details>

<details>
<summary>从 github 安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 输入以下命令克隆此储存库

    git clone https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin.git
  
打开 nonebot2 项目的 `bot.py` 文件, 在其中写入

    nonebot.load_plugin('src.plugins.nonebot_dcqq_relay_plugin')

</details>

# 感谢

- [nonebot/nonebot2](https://github.com/nonebot/nonebot2): 跨平台 Python 异步聊天机器人框架
- [koishijs/koishi-plugin-dcqq-relay](https://github.com/koishijs/koishi-plugin-dcqq-relay): 使用koishi实现同步Discord与QQ间的消息
- [Autuamn/nonebot-plugin-dcqg-relay](https://github.com/Autuamn/nonebot-plugin-dcqg-relay): 在QQ频道与 Discord 之间同步消息的 nonebot2 插件 [(抄了初始化的部分)](https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin/blob/main/nonebot_dcqq_relay_plugin/setup.py)