
from nonebot.plugin import PluginMetadata

#===============================================

__plugin_meta__ = PluginMetadata(
    name="nonebot_dcqq_relay_plugin",
    description="使用Nonebot2让Discord和QQ实现互相通信",
    usage=":<",
    type="application",
    extra={
        "author": "Github@Bottame [https://github.com/PawTeamClub]",
        "version": "1.0",
        "priority": 1,
    },
);

#===============================================

from .Setup import *
from .Event.QQ import *
from .Event.Discord import *

#===============================================

