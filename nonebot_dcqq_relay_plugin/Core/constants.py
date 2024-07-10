import re
from pathlib import Path
from nonebot import on_message, on_notice
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.onebot.v11 import Bot as OneBotBot

#======================================================

# 初始化 NoneBot
# 给初始化用的
class BotManager:
    OneBotObj: OneBotBot = None;
    DiscordBotObj: DiscordBot = None;
    webhook_id = None;
    webhook = None;
    DOWNLOAD_PATH: Path = None;
    DATABASE_PATH: Path = None;

bot_manager = BotManager()

#======================================================

# 常量
BOT_NAME = "nonebot_dcqq_bot";

# 正则表达
EMOJI_PATTERN = re.compile(r'<:(\w+):(\d+)>');                  #Discord Emoji
ENCODED_FACE_PATTERN = re.compile(r'&#91;([^&#]+)&#93;')        #QQ Mface Emoji
#======================================================

# 创建事件处理器
messageEvent = on_message(priority=10, block=True);
noticeEvent = on_notice(priority=5);