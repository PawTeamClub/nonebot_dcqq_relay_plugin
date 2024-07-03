from ..Data import GlobalVars, IConfig
from nonebot.log import logger
from nonebot.adapters.discord import Bot as DiscordBot#, MessageSegment as DiscordMessageSegment, Message as DiscordMessage
from nonebot.adapters.discord.event import MessageCreateEvent as DiscordMessageCreateEvent

@GlobalVars.messageEvent.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    if (not bool(GlobalVars.OneBotBotObj)):
        logger.debug("未找到OneBot");
        return

    if (event.channel_id != IConfig.plugin_config.discord_channel):
        logger.debug(f"频道ID与设置不对等 [事件频道id: {str(event.channel_id)} | 设置频道id: {IConfig.plugin_config.discord_channel}]");
        return
    
    # 此检测是为了防止转发机器人抽风
    # 然后其他机器人的消息也能转发过来
    if event.webhook_id == GlobalVars.webhook_id:
        logger.debug(f"检测Webhook [Webhookid: {event.webhook_id}]");
        return
    
    #====================================================================================================

    # 文本格式
    # [Bot Molu (Bottame)]:
    # Hi!

    #====================================================================================================

    message = f"[{event.member.nick} ({event.author.username})]:\n{event.content}"
    await GlobalVars.OneBotBotObj.send_group_msg(group_id=int(IConfig.plugin_config.onebot_channel), message=message)