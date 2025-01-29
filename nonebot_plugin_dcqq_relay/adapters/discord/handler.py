from typing                                 import Optional, Union
from nonebot.log                            import logger
from ...data.config                         import plugin_config
from ...data.globals                        import global_vars, event
from nonebot.adapters.discord               import Bot as DiscordBot
from nonebot.adapters.onebot.v11            import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.event         import MessageCreateEvent as DiscordMessageCreateEvent, MessageDeleteEvent as DiscordMessageDeleteEvent

def checkBot(bot: DiscordBot, event: Union[DiscordMessageCreateEvent, DiscordMessageDeleteEvent]) -> bool:
    # 如果没有连接到 OneBot 机器人，则不处理
    if (global_vars.onebot is None):
        return False;

    # 错误的频道或服务器
    if (event.channel_id != plugin_config.discord_channel) or (event.guild_id != plugin_config.discord_guild):
        return False;

    # 防止消息循环
    # Webhook 方面需要对 Event 进行判断
    if (global_vars.webhook is not None) and (isinstance(event, DiscordMessageCreateEvent)) and (event.webhook_id == global_vars.webhook.id):
        return False;

    return True;

async def getUserInfo(event: DiscordMessageCreateEvent) -> str:
    username = event.member.nick
    display_name = event.author.username or event.author.global_name
    return f"{display_name} ({username})" if display_name else str(username)

def getReplyId(event: DiscordMessageCreateEvent) -> Optional[str | int]:
    if (event.reply is None):
        return None;


    pass;
