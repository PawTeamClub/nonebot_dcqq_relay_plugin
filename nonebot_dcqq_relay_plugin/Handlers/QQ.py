
import asyncio
from Database.db import DiscordModule
from nonebot.log import logger
from config import plugin_config
from Adapters.QQ import QQ, formatImg
from Core.constants import messageEvent, bot_manager, noticeEvent
from nonebot.adapters.discord import Bot as DiscordBot#, MessageSegment as DiscordMessageSegment, Message as DiscordMessage
from nonebot.adapters.discord.event import MessageCreateEvent as DiscordMessageCreateEvent, MessageDeleteEvent as DiscordMessageDeleteEvent
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment

#====================================================================================================

@messageEvent.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    if not bot_manager.OneBotObj or not isinstance(event, DiscordMessageCreateEvent) or event.channel_id != plugin_config.discord_channel:
        return;

    # 此检测是为了防止转发机器人抽风
    if event.webhook_id == bot_manager.webhook_id:
        logger.debug(f"检测Webhook [Webhookid: {event.webhook_id}]");
        return;
    
    await DiscordModule.Create(str(event.id))

    QQFunc = QQ(userNick=event.member.nick, userName=event.author.username);

    #====================================================================================================

    # 文本格式
    # [Bot Molu (Bottame)]:
    # Hi!

    #====================================================================================================

    if event.attachments:
        for fileInfo in event.attachments:
            if fileInfo.content_type != "image/png":
                send_result = await QQFunc.sendFile(fileInfo);
                if send_result is not None:
                    for result in send_result:
                        if 'message_id' in result:
                            message_id = result.get("message_id")
                            logger.info(f"File sent with message_id: {message_id}")
                            await DiscordModule.Update(str(event.id), message_id)
                continue;
            result = await QQFunc.sendImage(fileInfo);
            await DiscordModule.Update(str(event.id), result.get("message_id"))

    if event.content:
        result = await QQFunc.sendGroup(formatImg(event.content));
        print(result.get("message_id"))
        await DiscordModule.Update(str(event.id), result.get("message_id"))

#@todo: delete_msg有异常，怀疑是Lagrange.Onebot的问题
@noticeEvent.handle()
async def handle_discord_delete_message(bot: DiscordBot, event: DiscordMessageDeleteEvent):
    if not bot_manager.OneBotObj or not isinstance(event, DiscordMessageDeleteEvent) or event.channel_id != plugin_config.discord_channel:
        return;

    messageList = await DiscordModule.Get(str(event.id))
    if not messageList or len(messageList) <= 0:
        return;

    for segment in messageList:
        await bot_manager.OneBotObj.delete_msg(message_id=int(segment));