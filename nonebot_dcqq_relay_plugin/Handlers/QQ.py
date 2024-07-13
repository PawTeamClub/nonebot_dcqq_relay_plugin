
from nonebot.log import logger

from nonebot_dcqq_relay_plugin.config import plugin_config
from nonebot_dcqq_relay_plugin.Adapters.QQ import QQ, formatImg
from nonebot_dcqq_relay_plugin.Database.db import DB, DiscordModule
from nonebot_dcqq_relay_plugin.Core.constants import messageEvent, bot_manager, noticeEvent

from nonebot.adapters.discord import Bot as DiscordBot#, MessageSegment as DiscordMessageSegment, Message as DiscordMessage
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.event import MessageCreateEvent as DiscordMessageCreateEvent, MessageDeleteEvent as DiscordMessageDeleteEvent

#====================================================================================================

@messageEvent.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    if not bot_manager.OneBotObj or not isinstance(event, DiscordMessageCreateEvent) or event.channel_id != plugin_config.discord_channel:
        return;

    await DiscordModule.Create(str(event.id))

    # 此检测是为了防止转发机器人抽风
    if event.webhook_id == bot_manager.webhook_id:
        logger.debug(f"检测Webhook [Webhookid: {event.webhook_id}]");
        return;

    QQFunc = QQ(userNick=event.member.nick, userName=event.author.username);
    ReplyID = None;
    resuleMessage = ""
    
    #====================================================================================================

    # 文本格式
    # [Bot Molu (Bottame)]:
    # Hi!

    #====================================================================================================

    # 看看有没有回复
    if event.reply:
        discordMessage = await DB.find_by_discord_message_id(str(event.reply.id))
        messageList = await DiscordModule.GetTables(str(event.reply.id))
        if discordMessage:
            ReplyID = discordMessage.onebot_message_id
        elif messageList:
            for segment in messageList:
                ReplyID = segment["id"];
                if segment["type"] == "file":
                    break;
        else:
            logger.warning("[Handlers_QQ] 获取Reply失败， 属性: ", str(event.reply))

    if ReplyID:
        resuleMessage += OneBotMessageSegment.reply(ReplyID)

    if event.content:
        resuleMessage += formatImg(event.content)

    if event.attachments:
        for fileInfo in event.attachments:
            # 图片
            if "image" in fileInfo.content_type.lower():
                resuleMessage += OneBotMessageSegment.image(fileInfo.url);
                continue;
            # 文件
            send_result = await QQFunc.sendFile(fileInfo);
            if send_result:
                message_id = next((result['message_id'] for result in send_result if 'message_id' in result), None)
                if message_id:
                    logger.info(f"File sent with message_id: {message_id}")
                    await DiscordModule.Update(str(event.id), message_id, "file")

    
    result = await QQFunc.sendGroup(OneBotMessage(resuleMessage));
    await DiscordModule.Update(str(event.id), result.get("message_id"), "content")
    

#@todo: delete_msg有异常，怀疑是Lagrange.Onebot的问题
@noticeEvent.handle()
async def handle_discord_delete_message(bot: DiscordBot, event: DiscordMessageDeleteEvent):
    if not bot_manager.OneBotObj or not isinstance(event, DiscordMessageDeleteEvent) or event.channel_id != plugin_config.discord_channel:
        return;

    # Discord撤回QQ用户消息
    discordMessage = await DB.find_by_discord_message_id(str(event.id))
    try:
        if discordMessage:
            await bot_manager.OneBotObj.delete_msg(message_id=int(discordMessage.onebot_message_id));
            return;
    except Exception as e:
        pass;
    
    # Discord用户自主撤回
    messageList = await DiscordModule.GetIDs(str(event.id))
    if not messageList or len(messageList) <= 0:
        return;

    for segment in messageList:
        await bot_manager.OneBotObj.delete_msg(message_id=int(segment));