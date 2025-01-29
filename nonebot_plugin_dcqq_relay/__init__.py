from nonebot.plugin import PluginMetadata
from nonebot.compat import PYDANTIC_V2

__plugin_meta__ = PluginMetadata(
    name="nonebot_dcqq_relay_plugin",
    description="使用Nonebot2让Discord和QQ群实现互相通信",
    usage=":<",
    type="application",
    homepage="https://github.com/PawTeamClub/nonebot_dcqq_relay_plugin",
    extra={
        "author": "Github@Robonyantame [https://github.com/PawTeamClub]",
        "version": "2.0",
        "priority": 1,
    },
);

from .setup import *
from .adapters import *
