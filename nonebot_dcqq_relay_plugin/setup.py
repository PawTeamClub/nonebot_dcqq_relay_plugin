#from pathlib import Path
from nonebot import get_driver
from nonebot.log import logger

from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.onebot.v11 import Bot as OneBotBot

from nonebot_dcqq_relay_plugin.config import plugin_config;
from nonebot_dcqq_relay_plugin.Database import DB
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager, BOT_NAME
from nonebot_dcqq_relay_plugin.Core.global_functions import cleanDownloadFolder, getPathFolder

#====================================================================================================

# 以下大部分代码是对着此项目复制的: https://github.com/Autuamn/nonebot-plugin-dcqg-relay/blob/main/nonebot_plugin_dcqg_relay/__init__.py
# 谢谢大神！
driver = get_driver()

@driver.on_startup
async def init():
    # 创建路径
    pathStr = plugin_config.data_dir + "/data/" if plugin_config.data_dir is not None else "./data/";
    logger.debug(f"Plugin Data Path: {pathStr}");
    MainPath = getPathFolder(pathStr);
    bot_manager.DOWNLOAD_PATH = getPathFolder(MainPath / "download");
    bot_manager.DATABASE_PATH = getPathFolder(MainPath / "db");
    # 初始化数据库
    await DB.init(bot_manager.DATABASE_PATH);

@driver.on_shutdown
async def clean_up():
    logger.info("机器人正在关闭...");
    # 关闭数据库
    await DB.close();
    # 清理下载文件夹
    cleanDownloadFolder(bot_manager.DOWNLOAD_PATH);

@driver.on_bot_connect
async def getDiscordBot(bot: DiscordBot):
    bot_manager.DiscordBotObj = bot;

@driver.on_bot_connect
async def getQQBot(bot: OneBotBot):
    bot_manager.OneBotObj = bot;

@driver.on_bot_connect
async def getWebhook(bot: DiscordBot):
    if not bot:
        return;

    webhooks = await bot.get_channel_webhooks(channel_id=int(plugin_config.discord_channel));
    webhookTemp = next((w for w in webhooks if w.name == BOT_NAME and w.user.username == bot.self_info.username), None);
    
    if bool(webhookTemp): 
        logger.debug("寻找到Webhook");
        bot_manager.webhook = webhookTemp;
        bot_manager.webhook_id = webhookTemp.id;
    else:
        logger.debug("没有寻找到Webhook, 正在创建");
        bot_manager.webhook = await bot.create_webhook(channel_id=int(plugin_config.discord_channel), name=BOT_NAME);
        bot_manager.webhook_id = bot_manager.webhook.id;