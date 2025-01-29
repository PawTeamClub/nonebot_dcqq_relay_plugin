from .handler                                   import *
from ...interfaces                              import Discord
from ...database.db                             import Database, OneBotModule
from ...data.globals                            import global_vars
from nonebot.adapters.onebot.v11.message        import MessageSegment

@event.message.handle()
async def handle_onebot_message(bot: OneBot, event: OneBotGroupMessageEvent):
    '''捕获群聊消息并转发到 Discord'''

    # 机器人是否中断
    if (await checkBot(bot, event) == False):
        return;

    # 往 OneBot 数据库添加消息ID，用于撤回
    # await OneBotModule.Create();

    # 初始化 OneBot 对象
    onebot = COneBot(bot, event.message_id, event)

    '''
    回复接口
        如果没有任何回复的消息，或者回复成功，为 True
        如果回复失败，为 False
        目前回复失败的原因有：
            1. 队列变量未初始化
            2. 解析 CQ 码或者解析回复 id 失败
            3. 创建 OneBot 对象时加入的事件出错
            4. 事件属于群文件上传事件
            5. 加入队列出现异常
    '''
    if (await onebot.reply(event.raw_message) is False):
        logger.error(f"回复发送失败！ qq={event.user_id} group={event.group_id} message={event.message}")

    '''
    格式化 CQ 码信息
        目前处理：
            1. 检测错误文本
            2. 检测图片、魔法表情以及 QQ 自己的表情包
            3. 检测 @ 某人
            4. 提示有未收录的 CQ 码
            5. 直接返回文本
    '''
    resultMessage = await process_message(bot, onebot, event)

    # 当 格式化消息为空时 或者 加入队列失败时，发送错误提示
    if (len(resultMessage) == 0) or (await onebot.text(resultMessage, None) is False):
        logger.error(f"消息发送失败！ qq={event.user_id} group={event.group_id} message={event.message}")


@event.notice.handle()
async def handle_group_upload(bot: OneBot, event: OneBotGroupUploadNoticeEvent):
    '''捕获群文件上传事件，将文件保存到本地并转发到 Discord'''

    # 机器人是否中断
    if (await checkBot(bot, event) == False):
        return;

@event.notice.handle()
async def handle_group_recall(bot: OneBot, event: OneBotGroupRecallNoticeEvent):
    '''捕获撤回事件，将消息从 Discord 同步删除'''

    if (global_vars.queue is None):
        return

    # 机器人是否中断
    if (await checkBot(bot, None) == False):
        return;

    # 撤回discord用户消息
    onebotMessageID = await Database.find_by_onebot_message_id(str(event.message_id));
    if onebotMessageID:
        if await global_vars.queue.put(
            content         = onebotMessageID.discord_message_id,
            msg_type        = "recallMessage",
            platform        = "discord",
            group_id        = plugin_config.discord_channel
        ) is False:
            logger.error(f"撤回消息放入队列失败: 目标消息ID={onebotMessageID.discord_message_id} 申请撤回群组={event.group_id} 撤回消息ID={event.message_id}")
            return False;

    # try:
    #     await Discord.deleteMessage();
    #     return;
    # except Exception as e:
    #     pass;

    # QQ用户自主撤回
    messageList = await OneBotModule.GetTables(event.message_id)
    if (not messageList) or (len(messageList) <= 0):
        return;

    for segment in messageList:
        if segment["type"] != "reply":
            if await global_vars.queue.put(
                content         = segment["id"],
                msg_type        = "recallWebHookMessage",
                platform        = "discord",
                group_id        = plugin_config.discord_channel
            ) is False:
                logger.error(f"撤回WebHook消息放入队列失败: 目标消息ID={segment["id"]} 申请撤回群组={event.group_id} 撤回消息ID={event.message_id}")
            continue;

        if await global_vars.queue.put(
            content         = segment["id"],
            msg_type        = "recallMessage",
            platform        = "discord",
            group_id        = plugin_config.discord_channel
        ) is False:
            logger.error(f"撤回消息放入队列失败: 目标消息ID={segment["id"]} 申请撤回群组={event.group_id} 撤回消息ID={event.message_id}")

        # if segment["type"] != "reply":
        #     await Discord.deleteWebhookMessage(segment["id"]);
        #     continue;
        # await Discord.deleteMessage(segment["id"]);
