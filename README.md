<p align="center">
  <img src="https://raw.githubusercontent.com/PawTeamClub/.github/main/paw_temporary_icons.png" width="200" height="200">
</p>

<div align="center">
  
# nonebot_dcqq_relay_plugin

<br />

_✨ 使用Nonebot2让Discord和QQ实现互相通信 ✨_

<br />

</div>

# 注意

此项目是基于onebot v11与discord适配器进行使用

目前此库还在开发阶段，所以不是很能用

~~被骂就被骂吧无所谓了~~

我不会打包成pip程序给nonebot2导入，先暂时这样吧()

你需要安装以下python库: `aiohttp | pathlib`

目前的测试平台是 `Nonebot2 + Lagrange.Onebot`

# 配置

## DISCORD_CHANNEL

**你可能需要开启Discord的开发者模式获取频道ID**

填写需要转发的Discord频道ID

[如果你不知道怎么开启开发者模式，点我](https://beebom.com/how-enable-disable-developer-mode-discord/#:~:text=Turn%20on%20Discord%20Developer%20Mode%20%28Android%2C%20iOS%29%201,access%20the%20IDs%20of%20channels%20and%20messages.%20)

```json
DISCORD_CHANNEL="123456789"
```

## ONEBOT_CHANNEL

填写需要转发的QQ群号

```json
ONEBOT_CHANNEL="123456789"
```

# TODO:

1. 撤回功能
2. 整理代码
3. at处理
4. 回复处理
