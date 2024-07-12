<p align="center">
  <img src="https://raw.githubusercontent.com/PawTeamClub/.github/main/paw_temporary_icons.png" width="200" height="200">
</p>

<div align="center">
  
# nonebot_dcqq_relay_plugin

<br />

_✨ 使用Nonebot2让Discord和QQ群实现互相通信 ✨_

<br />

</div>

# 注意

此项目是基于onebot v11与discord适配器进行使用，理论支持所有onebot v11项目

目前此插件还在开发阶段，所以不是很能用

**如果你在本插件开发的过程中使用，请做好每次更新都要删除数据库的打算 (**

我不会打包成pip程序给nonebot2导入，等做完基础的再研究

需要安装的库请查看requirements.txt

目前的测试平台是 `Nonebot2 + Lagrange.Onebot || NapCatQQ`

# 配置

## DISCORD_CHANNEL

**你可能需要开启Discord的开发者模式获取频道ID**

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

A2: 看[TODO第一条](#todo)

Q3: 为何不做多QQ群多频道转发

A3: 技术力不够~~因为懒~~

# TODO:

1. 撤回功能
    - Discord撤回onebot消息异常 (因为这是Lagrange.Onebot的bug, 暂时先记着)
        - 问题: delete_smg函数总是撤回消息的id和接收消息的id不一样  (在[Lagrange.Core/issues#226](https://github.com/LagrangeDev/Lagrange.Core/issues/226#issuecomment-2009693106)的回答中也遇到了这个问题，暂时没有解决方案 ~~我也不会C#~~)
        - 为什么不给Lagrange团队丢issue: 虽然issue那边是Core的问题，但因为问题冲突了所以我就不发了 ~~根本原因还是害怕挨骂和害怕交流~~
        - 在部分群是负值，但是在我自己的debug群确是正值就很奇怪
        - 使用LLOneBot、NapCatQQ框架测试时没有问题
    - onebot撤回Discord消息没有问题 (未仔细检查)
2. 同区域(discord回复discord、QQ回复QQ)好像没反应，明天检查
~~做几把@，做不了一点~~
