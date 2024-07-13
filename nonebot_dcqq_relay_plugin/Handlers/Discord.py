from nonebot.log import logger

from nonebot_dcqq_relay_plugin.config import plugin_config
from nonebot_dcqq_relay_plugin.Database import DB, QQModule
from nonebot_dcqq_relay_plugin.Core.constants import messageEvent, bot_manager, noticeEvent
from nonebot_dcqq_relay_plugin.Adapters.Discord import Discord, get_user_info, extract_cq
from nonebot_dcqq_relay_plugin.Core.global_functions import getFile

from nonebot.adapters.discord.api import File, MessageGet
from nonebot.adapters.onebot.v11 import (
    Bot as OneBotBot,
    GroupMessageEvent as OneBotGroupMessageEvent,
    #MessageSegment as OneBotMessageSegment,
    GroupRecallNoticeEvent as OneBotGroupRecallNoticeEvent,
    GroupUploadNoticeEvent as OneBotGroupUploadNoticeEvent
)

#====================================================================================================

# 消息事件
@messageEvent.handle()
async def handle_qq_message(bot: OneBotBot, event: OneBotGroupMessageEvent):
    if not bot_manager.DiscordBotObj or not isinstance(event, OneBotGroupMessageEvent) or event.group_id != plugin_config.onebot_channel:
        return
    
    await QQModule.Create(str(event.message_id));

    # 防止机器人自己转发自己的消息
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;

    #====================================================================================================

    # Webhook格式
    # 用户名：Robonyan_tame (QQ: 123456789):
    # 文本：Hi!

    #====================================================================================================
    user_name, avatar_url = await get_user_info(bot, event.group_id, event.user_id);
    DiscordFunc = Discord(user_name, avatar_url);

    #====================================================================================================

    # 回复
    reply_id = extract_cq("reply", event.raw_message)
    if reply_id:
        onebotReplyMessageID = await DB.find_by_onebot_message_id(reply_id);
        if onebotReplyMessageID:
            res = await DiscordFunc.reply(onebotReplyMessageID.discord_message_id);
            await QQModule.Update(str(event.message_id), res.id, "reply")
        else:
            QQDB = await QQModule.GetTables(reply_id)
            if QQDB is not None:
                segment = QQDB[-1]['id']
                logger.info(f"reply_id: {segment}")
                res = await DiscordFunc.reply(int(segment));
                await QQModule.Update(str(event.message_id), str(res.id), "reply")

    # 回复
    # None

    # 遍历信息获取常见CQ码
    for segment in event.message:
        logger.debug("segment.type: " + str(segment.type));
        if segment.type == "text" and not bool(segment.data.get('text')):           # 预防特殊事件导致脚本发生错误
            logger.warning(f"遇到无法处理的文本, 进行跳过处理 [内容: {repr(segment.data)}]");
            continue;
        elif segment.type in ["image", "mface", "face"]:                            # 表情
            res = await DiscordFunc.sendFace(segment)
            if res is not None:
                await QQModule.Update(str(event.message_id), res.id, "image")
        elif segment.type != "text":                                                # 孩子也不知道有啥要做的
            logger.debug(f"检测到 CQ 码：\n类型: {segment.type}\n数据: {segment.data}")
        else:                                                                       # 统统转文字处理
            logger.debug("segment.text: " + str(segment));
            res = await DiscordFunc.sendMessage(segment)
            await QQModule.Update(str(event.message_id), res.id, "content")

# 上传群文件事件
@noticeEvent.handle()
async def handle_group_upload(bot: OneBotBot, event: OneBotGroupUploadNoticeEvent):
    # 确保事件类型是群文件上传
    if not bot_manager.DiscordBotObj or not isinstance(event, OneBotGroupUploadNoticeEvent) or event.group_id != plugin_config.onebot_channel:
        return;
    # 防止机器人自己转发自己的消息
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;

    #====================================================================================================

    await QQModule.Create(str(event.message_id));
    user_name, avatar_url = await get_user_info(bot, event.group_id, event.user_id)
    DiscordFunc = Discord(user_name, avatar_url)
    
    file_info = await bot.get_group_file_url(group_id=event.group_id, file_id=event.file.id, busid=event.file.busid)
    file_url = file_info['url']

    #====================================================================================================

    FileBytes, FileStateCode = await getFile(file_url)
    if (FileBytes == None):
        error_message = (
            f"用户 {user_name} 上传了文件：\n"
            f"但是下载文件失败，请联系管理员重新下载文件，HTTP 状态码：{FileStateCode}"
        )
        res = await DiscordFunc.send(error_message)
        await QQModule.Update(str(event.message_id), res.id, "file")
        return;

    # File类格式化
    file = File(filename=event.file.name, content=FileBytes)
    res = await DiscordFunc.sendFile(user_name, avatar_url, file);
    await QQModule.Update(str(event.message_id), res.id, "file")

# 撤回事件
@noticeEvent.handle()
async def handle_group_recall(bot: OneBotBot, event: OneBotGroupRecallNoticeEvent):
    if not bot_manager.DiscordBotObj or not isinstance(event, OneBotGroupRecallNoticeEvent) or event.group_id != plugin_config.onebot_channel:
        return;

    # 撤回discord用户消息
    onebotMessageID = await DB.find_by_onebot_message_id(event.message_id);
    if onebotMessageID:
        try:
            await Discord.deleteMessage(onebotMessageID.discord_message_id);
            return;
        except Exception as e:
            pass;

    # QQ用户自主撤回
    messageList = await QQModule.GetTables(event.message_id)
    if not messageList or len(messageList) <= 0:
        return;
    
    for segment in messageList:
        if segment["type"] != "reply":
            await Discord.deleteWebhookMessage(segment["id"]);
            continue;
        await Discord.deleteMessage(segment["id"]);
        
    