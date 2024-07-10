from nonebot.log import logger
from config import plugin_config
from Core.global_functions import getFile
from nonebot.adapters.discord.api import File, MessageGet
from Adapters.Discord import Discord, get_user_info
from Core.constants import messageEvent, bot_manager, noticeEvent
from Database import DB, QQModule
from nonebot.adapters.onebot.v11 import (
    Bot as OneBotBot,
    GroupMessageEvent as OneBotGroupMessageEvent,
    #MessageSegment as OneBotMessageSegment,
    GroupRecallNoticeEvent as OneBotGroupRecallNoticeEvent,
    GroupUploadNoticeEvent as OneBotGroupUploadNoticeEvent
)

# 消息事件
@messageEvent.handle()
async def handle_qq_message(bot: OneBotBot, event: OneBotGroupMessageEvent):
    if not bot_manager.DiscordBotObj or not isinstance(event, OneBotGroupMessageEvent) or event.group_id != plugin_config.onebot_channel:
        return
    
    # 防止机器人自己转发自己的消息
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;

    #====================================================================================================

    # Webhook格式
    # 用户名：Robonyan_tame (QQ: 123456789):
    # 文本：Hi!

    #====================================================================================================

    await QQModule.Create(str(event.message_id));
    user_name, avatar_url = await get_user_info(bot, event.group_id, event.user_id);
    DiscordFunc = Discord(user_name, avatar_url);

    #====================================================================================================

    for segment in event.message:
        if segment.type == "text" and not bool(segment.data.get('text')):           # 预防特殊事件导致脚本发生错误
            logger.warning(f"遇到无法处理的文本, 进行跳过处理 [内容: {repr(segment.data)}]");
            continue;
        if segment.type in ["image", "mface", "face"]:
            res: MessageGet = await DiscordFunc.sendFace(segment)
            await QQModule.Update(str(event.message_id), res.id)
        elif segment.type != "text":                                                # 孩子也不知道有啥要做的
            logger.debug(f"检测到 CQ 码：\n类型: {segment.type}\n数据: {segment.data}")
        else:
            res: MessageGet = await DiscordFunc.sendMessage(segment)
            await QQModule.Update(str(event.message_id), res.id)

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
        await DiscordFunc.send(error_message)
        return;

    # File类格式化
    file = File(filename=event.file.name, content=FileBytes)
    res: MessageGet = await DiscordFunc.sendFile(user_name, avatar_url, file);
    await QQModule.Update(str(event.message_id), res.id)

# 撤回事件
@noticeEvent.handle()
async def handle_group_recall(bot: OneBotBot, event: OneBotGroupRecallNoticeEvent):
    if not bot_manager.DiscordBotObj or not isinstance(event, OneBotGroupRecallNoticeEvent) or event.group_id != plugin_config.onebot_channel:
        return;
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;

    messageList = await QQModule.Get(event.message_id)
    if not messageList or len(messageList) <= 0:
        return;
    
    for segment in messageList:
        await bot_manager.DiscordBotObj.delete_webhook_message(
            webhook_id=bot_manager.webhook_id,
            token=bot_manager.webhook.token,
            message_id=segment
        )
    