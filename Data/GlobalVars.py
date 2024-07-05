from nonebot import on_message, on_notice
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.onebot.v11 import Bot as OneBotBot
from pathlib import Path

BOT_NAME = "nonebot_dcqq_bot";

# 初始化 NoneBot
# 给初始化用的
OneBotBotObj: OneBotBot = None;
DiscordBotObj: DiscordBot = None;
webhook_id = None;
webhook = None;
DOWNLOAD_PATH: Path = None;

# 配置
# 除了webhook名字其他都会塞进env进行配置
DISCORD_CHANNEL_ID = "1123601828794343536";
QQ_GROUP_ID = "138889370";

# 创建事件处理器
messageEvent = on_message(priority=10, block=True);
noticeEvent = on_notice(priority=5);