import json
from typing                             import Optional, Union
from ...utils                           import extract_cq, generateRandomString
from ...database                        import Database, OneBotModule
from nonebot.log                        import logger
from ...data.config                     import plugin_config
from ...data.globals                    import global_vars, event
from ...data.pattern                    import FACE
from nonebot.adapters.onebot.v11        import (Bot as OneBot, MessageSegment as OneBotMessageSegment, GroupMessageEvent as OneBotGroupMessageEvent, GroupRecallNoticeEvent as OneBotGroupRecallNoticeEvent, GroupUploadNoticeEvent as OneBotGroupUploadNoticeEvent)
from nonebot.adapters.discord.api       import File, MessageGet, MessageReference

async def checkBot(bot: OneBot, event: Optional[Union[OneBotGroupMessageEvent, OneBotGroupUploadNoticeEvent]]) -> bool:
    '''
    检测机器人是否该处理消息

    :param bot: 机器人对象
    :param event: 事件对象

    :return: 是否处理消息
    '''
    # 如果没有连接到 Discord 机器人，则不处理
    if (global_vars.discord_bot is None):
        return False;

    # 防止获取非指定群聊的消息
    if (event is not None) and (event.group_id != plugin_config.onebot_channel):
        return False;

    # 防止消息循环
    login_info = await bot.get_login_info()
    if (event is not None) and (event.user_id == login_info["user_id"]):
        return False;

    return True;

async def getUserInfo(bot: OneBot, group_id: int, user_id: int) -> tuple[str, str]:
    '''
    获取用户消息并格式化成Webhook需要的内容

    :param bot: OneBot机器人对象
    :param group_id: 指定群号
    :param user_id: 需要查询的用户 QQ 号

    :return: 用户信息
    '''
    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)
    user_name = f"{user_info['card'] or user_info['nickname']} (QQ: {user_id})"
    avatar_url = f"http://q.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640"
    return user_name, avatar_url

class COneBot:
    async def __init__(self, bot: OneBot, message_id: int, event: Union[OneBotGroupMessageEvent, OneBotGroupUploadNoticeEvent, OneBotGroupRecallNoticeEvent]):
        self.bot = bot
        self.event = event
        self.message = None
        self.message_id = message_id
        self.user_id = event.user_id
        self.group_id = event.group_id
        user_name, avatar_url = await getUserInfo(bot, self.group_id, self.user_id)
        self.user_name = user_name
        self.avatar_url = avatar_url

    async def reply(self, message_raw: str) -> bool:
        # 如果队列未初始化则直接返回
        if (global_vars.queue is None):
            logger.error("队列对象未初始化，无法处理消息")
            return False;

        # 解析回复的 CQ 码
        id = extract_cq("reply", message_raw)

        # 如果 CQ 码为空或者事件为空或者是错误的事件则直接返回
        if (id is None) or (self.event is None) or isinstance(self.event, OneBotGroupUploadNoticeEvent):
            return False;

        # 从 OneBot 消息索引数据库获取消息ID
        onebotReplyMessageID = await Database.find_by_onebot_message_id(id);
        reply_segment = None;

        # 如果 OneBot 消息ID不为空则直接获取
        if onebotReplyMessageID is not None:
            reply_segment = int(onebotReplyMessageID.discord_message_id);
        # 否则尝试从全局消息索引数据库中获取
        else:
            QQDB = await OneBotModule.GetTables(id)
            if QQDB is not None and len(QQDB) > 0:
                segment = QQDB[-1]['id']
                reply_segment = int(segment);

        # 如果未找到需要回复的消息则直接返回
        if (reply_segment is None):
            return True;

        # 添加队列
        if await global_vars.queue.put(
            meg_id          = self.message_id,
            content         = f"{self.user_name} replied to this message!",
            msg_type        = "reply",
            platform        = "discord",
            group_id        = plugin_config.discord_channel,
            username        = self.user_name,
            avatar_url      = self.avatar_url
        ) is False:
            logger.error(f"消息放入队列失败: qq={self.event.user_id} group={self.event.group_id} message={event.message}")
            return False;

        return True;

        # res = await self._reply(reply_segment);
        # if (res is None):
        #     logger.error("Error replying to message");
        #     return;

        # await OneBotModule.Update(str(self.event.message_id), str(res.id), "reply")

    async def image(self, segment: OneBotMessageSegment) -> bool:
        if global_vars.queue is None:
            return False;

        # 有待优化
        #file_byte, file_status_code, file_type = await getHttpxFile(segment.data['url'])
        file_status_code, file_type = "1", "image"
        file_byte: bytes = bytes(10)
        if (file_status_code != 200) or ("image" not in file_type):
            logger.error(f"获取图片失败 (状态码: {file_status_code}, 文件类型: {file_type}")
            return False;

        # 在想是传字节码好还是文件好
        # 将内容打包成 JSON，好放入队列
        file_data = {
            # 因为 http 的结果带有头，我们可以通过头部信息来获取此文件具体是什么文件类型，所以按照这个情况进行了字符串格式化
            "filename": generateRandomString() + f".{file_type}",
            "content": file_byte
        }
        json_string = json.dumps(file_data, ensure_ascii=False)

        # 防止打包失败
        if json_string is None:
            logger.error(f"图片转换失败 [图片类型: {file_type}]")
            return False;

        if await global_vars.queue.put(
            meg_id          = self.message_id,
            content         = json_string,
            msg_type        = "image",
            platform        = "discord",
            group_id        = plugin_config.discord_channel,
            username        = self.user_name,
            avatar_url      = self.avatar_url
        ) is False:
            logger.error(f"图片放入队列失败: qq={self.event.user_id} group={self.event.group_id}")
            return False;

        return True;

    async def file(self) -> bool:
        if global_vars.queue is None:
            return False;

        if not isinstance(self.event, OneBotGroupUploadNoticeEvent):
            return False;

        # NapCat补上接口了，感谢上帝
        file_info = await self.bot.get_group_file_url(group_id=self.event.group_id, file_id=self.event.file.id, busid=self.event.file.busid)
        if file_info is None:
            return False;

        file_url = file_info['url']

        # FileBytes, FileStateCode = await getFile(file_url)
        file_bytes, file_state_code = bytes(10), 100

        # 感觉这个问题十分重要，还是加上吧
        # 如果没有获得文件字节码，那么就给转发的指定服务器进行提示，让管理员进行处理
        if (file_bytes is None):
            error_message = (
                 f"用户 {self.user_name} 上传了文件：\n"
                 f"但是下载文件失败，请联系管理员重新下载文件，HTTP 状态码：{file_state_code}"
            )
            await self.text(error_message, "file")
            return False

        # 将内容打包成 JSON，好放入队列
        file_data = {
            "filename": self.event.file.name,
            "content": file_bytes
        }
        json_string = json.dumps(file_data, ensure_ascii=False)

        # 防止打包失败
        if json_string is None:
            logger.error(f"文件转换失败 [文件名: {self.event.file.name}]")
            return False;

        if await global_vars.queue.put(
            meg_id          = self.message_id,
            content         = json_string,
            msg_type        = "file",
            platform        = "discord",
            group_id        = plugin_config.discord_channel,
            username        = self.user_name,
            avatar_url      = self.avatar_url
        ) is False:
            logger.error(f"文件放入队列失败: qq={self.event.user_id} group={self.event.group_id} filename={self.event.file.name}")
            return False;

        return True;

    async def text(self, message: str, force_type: Optional[str]) -> bool:
        if (global_vars.queue is None):
            logger.error("队列对象未初始化，无法处理消息")
            return False;

        # 去掉表情 CQ 码
        new_message = FACE.sub('', message)

        # 防止去掉后空字符串
        if bool(new_message.strip()) is False:
            return True;

        if await global_vars.queue.put(
            meg_id          = self.message_id,
            content         = new_message,
            msg_type        = force_type or "message",
            platform        = "discord",
            group_id        = plugin_config.discord_channel,
            username        = self.user_name,
            avatar_url      = self.avatar_url
        ) is False:
            logger.error(f"消息放入队列失败: qq={self.event.user_id} group={self.event.group_id} message={event.message}")
            return False;

        return True;

async def process_message_segment(bot: OneBot, cbot: COneBot, segment: OneBotMessageSegment, event: OneBotGroupMessageEvent) -> str:
    ''' 格式化消息段 '''

    # 处理空文本
    if segment.type == "text" and not segment.data.get('text'):
        logger.warning(f"遇到无法处理的文本, 进行跳过处理 [内容: {repr(segment.data)}]")
        return ""

    # 处理图片文件
    if segment.type == "image":
        await cbot.image(segment)
        return ""

    # 处理 QQ 魔法表情
    if segment.type == "mface":
        return segment.data['url']

    # 处理 QQ 表情
    # 拿 Github 当图床我觉得一点问题都没有 (?)
    if segment.type == "face":
        emojiURL = f"https://robonyantame.github.io/QQEmojiFiles/Image/{segment.data.get('id')}.gif"
        return emojiURL

    # 处理 @ 消息
    if segment.type == "at":
        if qq := segment.data.get("qq"):
            at_user_name, _ = await getUserInfo(bot, event.group_id, int(qq))
            return f"`@{at_user_name}` "
        return ""

    # 下面两条暂时不做
    if segment.type == "record":
        pass

    if segment.type == "video":
        pass

    # 处理其他非文本消息
    # Debug 用
    if segment.type != "text":
        logger.debug(f"检测到 CQ 码：\n类型: {segment.type}\n数据: {segment.data}")
        return ""

    # 处理普通文本
    return str(segment)

async def process_message(bot: OneBot, cbot: COneBot, event: OneBotGroupMessageEvent) -> str:
    ''' 格式化消息 '''
    result_message = ""
    for segment in event.message:
        # Debug
        logger.debug(f"segment.type: {segment.type}")
        result_message += await process_message_segment(bot, cbot, segment, event)
    return result_message
