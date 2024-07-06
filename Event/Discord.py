from ..Utility import GlobalFuns
from ..Data import GlobalVars
from ..Data.IConfig import plugin_config
from ..Utility import Discord
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot as OneBotBot, GroupMessageEvent as OneBotGroupMessageEvent, MessageSegment as OneBotMessageSegment, GroupUploadNoticeEvent as OneBotGroupUploadNoticeEvent
from nonebot.adapters.discord.api import File

@GlobalVars.messageEvent.handle()
async def handle_qq_message(bot: OneBotBot, event: OneBotGroupMessageEvent):
    if (not bool(GlobalVars.DiscordBotObj)):
        return;
    if event.group_id != plugin_config.onebot_channel:
        return;
    
    # 防止机器人自己转发自己的消息
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;
    
    #====================================================================================================

    # Webhook格式
    # 用户名：Robonyan_tame (QQ: 123456789):
    # 文本：Hi!

    #====================================================================================================

    user_id = event.sender.user_id;
    user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=user_id, no_cache=True);     # 事件的用户信息带有缓存，以防更新不及时先这样挂着
    user_name = f"{user_info['card'] or user_info['nickname']} (QQ: {user_id})";
    avatar_url = f"http://q.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640";

    #====================================================================================================

    # 预防特殊事件导致脚本发生错误
    for segment in event.message:
        if segment.type == "image" or segment.type == "mface":        # 图片和自定义表情
            await Discord.sendMeg(user_name, avatar_url, segment.data['url'])
        elif segment.type == "face":                                  # 表情
            # 自己收集的表情
            # https://github.com/Robonyantame/QQEmojiFiles
            emojiURL = f"https://robonyantame.github.io/QQEmojiFiles/Image/{segment.data.get('id')}.gif"
            # 防止没有表情然后发送链接
            Filebyte, FileStatusCode = await GlobalFuns.getFile(emojiURL)
            if FileStatusCode == 200:
                await Discord.sendMeg(user_name, avatar_url, emojiURL)
        # Debug Mode
        elif segment.type != "text":
            # 这是一个 CQ 码
            cq_type = segment.type;
            cq_data = segment.data;
            logger.debug(f"检测到 CQ 码：\n类型: {cq_type}\n数据: {cq_data}")
        elif not bool(segment.data.get('text')):
            logger.warning(f"遇到无法处理的文本, 进行跳过处理 [内容: {repr(segment.data)}]");
            return;
        else:
            # 都怪mface
            cleaned_text = Discord.remove_encoded_faces(str(segment))
            if cleaned_text.strip():  # 只有在清理后的文本不为空时才发送
                await Discord.sendMeg(user_name, avatar_url, cleaned_text)


@GlobalVars.noticeEvent.handle()
async def handle_group_upload(bot: OneBotBot, event: OneBotGroupUploadNoticeEvent):
    # 确保事件类型是群文件上传
    if not isinstance(event, OneBotGroupUploadNoticeEvent):
        return;
    if event.group_id != plugin_config.onebot_channel:
        return
    # 防止机器人自己转发自己的消息
    login_info = await bot.get_login_info()
    if event.user_id == login_info["user_id"]:
        return;

    #====================================================================================================
    # 好长的一坨

    group_id = event.group_id;
    user_id = event.user_id;
    file_id = event.file.id;
    file_name = event.file.name;

    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    file_info = await bot.get_group_file_url(group_id=group_id, file_id=file_id, busid=event.file.busid);
    file_url = file_info['url']

    user_name = f"{user_info['card'] or user_info['nickname']} (QQ: {user_id})";
    avatar_url = f"http://q.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640";

    #====================================================================================================

    FileBytes, FileStateCode = await GlobalFuns.getFile(file_url)
    if (FileBytes == None):
        # 重下的东西在想吧，有点懒
        stateCode = f"，HTTP 状态码：{FileStateCode}"
        errorMessage = f"用户 {user_name} 上传了文件：\n"
        errorMessage += f"但是下载文件失败，请联系管理员重新下载文件{stateCode}"
        await GlobalVars.DiscordBotObj.send_to(channel_id=int(plugin_config.discord_channel), message=errorMessage)
        return;

    # File类格式化
    file = File(
        filename=file_name, 
        content=FileBytes
    )

    await Discord.sendFile(user_name, avatar_url, file);