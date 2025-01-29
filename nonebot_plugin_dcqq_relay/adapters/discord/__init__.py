from .handler import *

@event.message.handle()
async def handle_discord_message(bot: DiscordBot, event: DiscordMessageCreateEvent):
    # 机器人是否中断
    if (checkBot(bot, event) == False):
        return;

    # 转发消息
    if event.attachments is not None:
        for attachment in event.attachments:
            if attachment.content_type is not None:
                pass
            pass

@event.notice.handle()
async def handle_discord_delete_message(bot: DiscordBot, event: DiscordMessageDeleteEvent):
    # 机器人是否中断
    if (checkBot(bot, event) == False):
        return;

    # 删除消息
    pass
