from ..Data import GlobalVars
from nonebot.adapters.discord.api import File

# Discord -> 发送纯文本消息
async def sendMeg(username: str, avatar_url:str, message: str):
    await GlobalVars.DiscordBotObj.execute_webhook(
            webhook_id= GlobalVars.webhook.id,
            token= GlobalVars.webhook.token,
            username= username or "Unknown User (WTF???)",
            avatar_url= avatar_url,
            content=message
    );

# Discord -> 发送单文件
async def sendFile(username: str, avatar_url:str, Files: File):
    await GlobalVars.DiscordBotObj.execute_webhook(
            webhook_id= GlobalVars.webhook.id,
            token= GlobalVars.webhook.token,
            username= username or "Unknown User (WTF???)",
            avatar_url= avatar_url,
            files=[Files]
    );

# Discord -> 发送多文件 (目前没什么作用)
async def sendFiles(username: str, avatar_url:str, Files: list[File]):
    await GlobalVars.DiscordBotObj.execute_webhook(
            webhook_id= GlobalVars.webhook.id,
            token= GlobalVars.webhook.token,
            username= username or "Unknown User (WTF???)",
            avatar_url= avatar_url,
            files=Files
    );