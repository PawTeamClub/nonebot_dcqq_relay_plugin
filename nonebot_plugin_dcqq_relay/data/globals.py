from typing                             import Optional
from ..utils                            import getPathFolder, Queue
from .config                            import plugin_config
from nonebot                            import on_message, on_notice
from nonebot.adapters.discord           import Bot as DiscordBot
from nonebot.adapters.onebot.v11        import Bot as OneBotBot
from nonebot.adapters.discord.api       import Webhook

class Events:
    def __init__(self):
        self.notice             = on_notice(priority=5)
        self.message            = on_message(priority=10, block=True)

class GlobalVars:
    def __init__(self):
        self.queue:             Optional[Queue] = None
        self.onebot:            Optional[OneBotBot] = None
        self.webhook:           Optional[Webhook] = None
        self.discord_bot:       Optional[DiscordBot] = None

class Path:
    def __init__(self):
        pathStr = plugin_config.data_dir + "/data/" if plugin_config.data_dir is not None else "./data/";
        self.Main = getPathFolder(pathStr);
        if (self.Main is None):
            return;
        self.download   = getPathFolder(self.Main / "download");
        self.database   = getPathFolder(self.Main / "db");
        self.temp       = getPathFolder(self.Main / "temp");

global_vars = GlobalVars();
event = Events();
path = Path();
