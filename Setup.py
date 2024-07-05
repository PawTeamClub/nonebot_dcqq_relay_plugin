from .Data import GlobalVars, IConfig
from nonebot import get_bots
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from pathlib import Path

# 加载 OneBot 适配器
# 由于nonebot_discord_adapter的特殊性，他要使用心跳包接受bot的信息才能正常使用，所以我使用了计时器来让discord bot正常获取
# 在思考要不要把这里丢进消息事件中
# 这里应该有更好的优化方式，但是我真的不是很了解nonebot这玩意
@scheduler.scheduled_job("interval", seconds=5, id="job_0")
async def init():
    
    # 获取所有bot
    bots = get_bots();

    # 如果加载不到bot列表，那就直接中断
    # 还是因为不知道适配器是否有相应时间的问题
    if not bool(bots):
        return False;

    GlobalVars.DiscordBotObj = next((bot for bot in bots.values() if bot.type == "Discord"), None);
    if not GlobalVars.DiscordBotObj:
        logger.warning("未找到所需的Discord机器人，将在下次执行时重试");
        return;

    GlobalVars.OneBotBotObj = next((bot for bot in bots.values() if bot.type == "OneBot V11"), None);
    if not GlobalVars.OneBotBotObj:
        logger.warning("未找到所需的OneBot机器人，将在下次执行时重试");
        return;
    
    # 通过频道id查询webhook列表
    # 如果没有创建那就创建，如果有那就直接用
    webhooks = await GlobalVars.DiscordBotObj.get_channel_webhooks(channel_id=int(IConfig.plugin_config.discord_channel));
    webhookTemp = next((w for w in webhooks if w.name == GlobalVars.BOT_NAME), None);
    if bool(webhookTemp): 
        logger.debug("寻找到Webhook");
        GlobalVars.webhook = webhookTemp;
        GlobalVars.webhook_id = webhookTemp.id;
    else:
        logger.debug("没有寻找到Webhook, 正在创建");
        GlobalVars.webhook = await GlobalVars.DiscordBotObj.create_webhook(channel_id=int(IConfig.plugin_config.discord_channel), name=GlobalVars.BOT_NAME);
        GlobalVars.webhook_id = GlobalVars.webhook.id;

    path = Path() / "data" / "download";
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True);
    GlobalVars.DOWNLOAD_PATH = path;

    # 关闭计时器
    scheduler.shutdown();

