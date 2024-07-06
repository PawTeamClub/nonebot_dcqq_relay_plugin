from ..Utility.QQ import QQ, formatImg
from ..Data import GlobalVars
from ..Data.IConfig import plugin_config
from nonebot.log import logger
from nonebot.adapters.discord import Bot as DiscordBot#, MessageSegment as DiscordMessageSegment, Message as DiscordMessage
from nonebot.adapters.discord.event import MessageCreateEvent as DiscordMessageCreateEvent

@GlobalVars.messageEvent.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    if (not bool(GlobalVars.OneBotBotObj)):
        logger.debug("未找到OneBot");
        return;

    if (event.channel_id != plugin_config.discord_channel):
        logger.debug(f"频道ID与设置不对等 [事件频道id: {str(event.channel_id)} | 设置频道id: {plugin_config.discord_channel}]");
        return;
    
    # 此检测是为了防止转发机器人抽风
    # 然后其他机器人的消息也能转发过来
    if event.webhook_id == GlobalVars.webhook_id:
        logger.debug(f"检测Webhook [Webhookid: {event.webhook_id}]");
        return;
    
    QQFunc = QQ(userNick=event.member.nick, userName=event.author.username);

    #====================================================================================================

    # 文本格式
    # [Bot Molu (Bottame)]:
    # Hi!

    #====================================================================================================

    # 先瞎写
    if len(event.attachments) > 0:
        for fileInfo in event.attachments:
            # 发送图片
            if fileInfo.content_type == "image/png":
                await QQFunc.sendImage(fileInfo.url);
                continue;
            # 下载文件
            await QQFunc.sendFile(fileInfo);

    if len(event.content) <= 0:
        return;

    await QQFunc.sendGroup(formatImg(event.content));