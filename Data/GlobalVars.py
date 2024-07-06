from pathlib import Path
from nonebot import on_message, on_notice
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.onebot.v11 import Bot as OneBotBot

#======================================================

# 初始化 NoneBot
# 给初始化用的
OneBotBotObj: OneBotBot = None;
DiscordBotObj: DiscordBot = None;
webhook_id = None;
webhook = None;

#======================================================

# 常量
BOT_NAME = "nonebot_dcqq_bot";
DOWNLOAD_PATH: Path = None;

#======================================================

# 创建事件处理器
messageEvent = on_message(priority=10, block=True);
noticeEvent = on_notice(priority=5);