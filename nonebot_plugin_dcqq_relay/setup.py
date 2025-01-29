from .utils                             import cleanFolder, Queue
from pathlib                            import Path
from asyncio                            import sleep
from nonebot                            import get_driver
from .database                          import Database
from nonebot.log                        import logger
from .data.config                       import plugin_config
from .data.globals                      import global_vars, path
from nonebot.adapters.discord           import Bot as DiscordBot
from nonebot.adapters.onebot.v11        import Bot as OneBotBot

driver          = get_driver()
BOT_NAME        = "nonebot_dcqq_bot";

@driver.on_startup
async def on_init():
    """初始化数据库"""
    if path.database is None:
        logger.error("数据库路径为空");
        return;

    await Database.init(path.database);
    global_vars.queue = Queue();

@driver.on_shutdown
async def on_shutdown():
    logger.info("机器人正在关闭...");
    # 关闭数据库
    await Database.close();

    # 清理下载文件夹
    if path.download is None:
        logger.error("下载路径为空");
        return;

    cleanFolder(path.download);

    if global_vars.queue is not None:
        await global_vars.queue.cleanup_processed_messages();

# @todo: 需要debug
@driver.on_bot_disconnect
async def on_bot_disconnect(bot: DiscordBot):
    if global_vars.discord_bot is None:
        return;
    logger.info("Discord机器人已断开连接:", bot)
    await global_vars.discord_bot.adapter.shutdown();
    logger.info("五秒后尝试重新链接discord...")
    await sleep(5);
    await global_vars.discord_bot.adapter.startup();

@driver.on_bot_connect
async def on_onebot_connect(bot: OneBotBot):
    global_vars.onebot = bot
    logger.info("OneBot机器人已连接:", bot)

@driver.on_bot_connect
async def on_bot_connect(bot: DiscordBot):
    global_vars.discord_bot = bot
    logger.info("Discord机器人已连接:", bot)

    # 获取Webhook
    webhooks = await bot.get_channel_webhooks(channel_id=int(plugin_config.discord_channel));
    webhook_find = next((w for w in webhooks if w.name == BOT_NAME and w.user.username == bot.self_info.username), None);

    if webhook_find is not None:
        logger.debug("寻找到Webhook");
        global_vars.webhook = webhook_find;
        return;

    logger.debug("没有寻找到Webhook, 正在创建");
    global_vars.webhook = await bot.create_webhook(channel_id=int(plugin_config.discord_channel), name=BOT_NAME);
