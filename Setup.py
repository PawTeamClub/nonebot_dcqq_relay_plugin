from pathlib import Path
from .Data import GlobalVars
from nonebot import get_driver
from nonebot.log import logger
from .Data.IConfig import plugin_config;
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.onebot.v11 import Bot as OneBotBot

# 以下大部分代码是对着此项目复制的: https://github.com/Autuamn/nonebot-plugin-dcqg-relay/blob/main/nonebot_plugin_dcqg_relay/__init__.py
# 谢谢大神！
driver = get_driver()

path = Path() / "data" / "download";
if not path.exists():
    path.mkdir(parents=True, exist_ok=True);
GlobalVars.DOWNLOAD_PATH = path;

@driver.on_bot_connect
async def getDiscordBot(bot: DiscordBot):
    GlobalVars.DiscordBotObj = bot

@driver.on_bot_connect
async def getQQBot(bot: OneBotBot):
     GlobalVars.OneBotBotObj = bot

@driver.on_bot_connect
async def getWebhook(bot: DiscordBot):
    if not bot:
        return;

    webhooks = await bot.get_channel_webhooks(channel_id=int(plugin_config.discord_channel));
    webhookTemp = next((w for w in webhooks if w.name == GlobalVars.BOT_NAME), None);
    if bool(webhookTemp): 
        logger.debug("寻找到Webhook");
        GlobalVars.webhook = webhookTemp;
        GlobalVars.webhook_id = webhookTemp.id;
    else:
        logger.debug("没有寻找到Webhook, 正在创建");
        GlobalVars.webhook = await bot.create_webhook(channel_id=int(plugin_config.discord_channel), name=GlobalVars.BOT_NAME);
        GlobalVars.webhook_id = GlobalVars.webhook.id;