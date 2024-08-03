
from nonebot.log import logger

from nonebot_dcqq_relay_plugin.config import plugin_config
from nonebot_dcqq_relay_plugin.Adapters.QQ import QQ, formatEmoji, formatAT
from nonebot_dcqq_relay_plugin.Database.db import DB, DiscordModule
from nonebot_dcqq_relay_plugin.Core.constants import messageEvent, bot_manager, noticeEvent
from nonebot_dcqq_relay_plugin.Core.global_functions import apngToGif, lottieToGif

from nonebot.adapters.discord import Bot as DiscordBot#, MessageSegment as DiscordMessageSegment, Message as DiscordMessage
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.event import MessageCreateEvent as DiscordMessageCreateEvent, MessageDeleteEvent as DiscordMessageDeleteEvent

#====================================================================================================

@messageEvent.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    if not bot_manager.OneBotObj or not isinstance(event, DiscordMessageCreateEvent) or event.channel_id != plugin_config.discord_channel or event.guild_id != plugin_config.discord_guild:
        return;

    # 此检测是为了防止转发机器人抽风
    if event.webhook_id == bot_manager.webhook_id:
        logger.debug(f"检测Webhook [Webhookid: {event.webhook_id}]");
        return;

    await DiscordModule.Create(str(event.id))

    QQFunc = QQ(userNick=event.member.nick, globalName=event.author.global_name ,userName=event.author.username);
    ReplyID = None;
    resuleMessage = ""
    
    #====================================================================================================

    # 文本格式
    # [Bot Molu (Bottame)]:
    # Hi!

    #====================================================================================================

    # 查看回复
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

    # 消息内容
    if event.content:
        formatted_at = await formatAT(event.content)
        resuleMessage += formatEmoji(formatted_at)

    # 贴纸
    if event.sticker_items:
        for sticker in event.sticker_items:
            if sticker.format_type.value in [1, 4]:                         # PNG/GIF
                extension = 'png' if sticker.format_type.value == 1 else 'gif'
                resuleMessage += OneBotMessageSegment.image(f"https://media.discordapp.net/stickers/{sticker.id}.{extension}")
            elif sticker.format_type.value == 2:                            # APNG
                gifPath = await apngToGif(sticker.id)
                if not gifPath:
                    continue;
                resuleMessage += OneBotMessageSegment.image(gifPath)
            elif sticker.format_type.value == 3:                            # Lottie
                lottiePath = await lottieToGif(sticker.id)
                if not lottiePath:
                    continue;
                resuleMessage += OneBotMessageSegment.image(lottiePath);

    # Discord嵌入式图片
    if event.embeds:
        for embed in event.embeds:
            embedType = embed.type;
            if embedType == "gifv" and embed.video is not None:
                gifFile = await QQFunc.getGIFFile(embed.video.url);
                resuleMessage += OneBotMessageSegment.image(gifFile)
            elif embedType == "image" and embed.thumbnail is not None:
                resuleMessage += OneBotMessageSegment.image(embed.thumbnail.url)

    # 附件
    if event.attachments:
        for fileInfo in event.attachments:
            # 图片
            if fileInfo.content_type and "image" in fileInfo.content_type.lower():
                resuleMessage += OneBotMessageSegment.image(fileInfo.url);
                continue;
            # 文件
            send_result = await QQFunc.sendFile(fileInfo);
            if send_result:
                message_id = next((result['message_id'] for result in send_result if 'message_id' in result), None)
                if message_id:
                    logger.info(f"File sent with message_id: {message_id}")
                    await DiscordModule.Update(str(event.id), message_id, "file")

    # 发送消息
    if resuleMessage:
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
            discordMessageID = int(discordMessage.onebot_message_id)
            msg = await bot_manager.OneBotObj.get_msg(message_id=discordMessageID)
            if msg:
                await bot_manager.OneBotObj.delete_msg(message_id=discordMessageID);
            return;
    except Exception as e:
        pass;
    
    # Discord用户自主撤回
    messageList = await DiscordModule.GetIDs(str(event.id))
    if not messageList or len(messageList) <= 0:
        return;

    for segment in messageList:
        messageID = int(segment);
        msg = await bot_manager.OneBotObj.get_msg(message_id=messageID)
        if msg:
            await bot_manager.OneBotObj.delete_msg(message_id=messageID);