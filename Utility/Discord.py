import re
from ..Data import GlobalVars
from nonebot.adapters.discord.api import File

# 用于匹配编码的表情文本的正则表达式
ENCODED_FACE_PATTERN = re.compile(r'&#91;([^&#]+)&#93;')

# 移除编码的表情文本
def remove_encoded_faces(text: str) -> str:
    return ENCODED_FACE_PATTERN.sub('', text)

class Discord():
    username: str;
    avatar_url:str;

    def __init__(self, username: str, avatar_url:str):
        self.username = username;
        self.avatar_url = avatar_url;

    # Discord -> 发送纯文本消息
    async def sendMeg(self, message: str):
        await GlobalVars.DiscordBotObj.execute_webhook(
                webhook_id= GlobalVars.webhook.id,
                token= GlobalVars.webhook.token,
                username= self.username or "Unknown User (WTF???)",
                avatar_url= self.avatar_url,
                content=message
        );


    # Discord -> 发送单文件
    async def sendFile(self, Files: File):
        await GlobalVars.DiscordBotObj.execute_webhook(
                webhook_id= GlobalVars.webhook.id,
                token= GlobalVars.webhook.token,
                username= self.username or "Unknown User (WTF???)",
                avatar_url= self.avatar_url,
                files=[Files]
        );

    # Discord -> 发送多文件 (目前没什么作用)
    async def sendFiles(self, Files: list[File]):
        await GlobalVars.DiscordBotObj.execute_webhook(
                webhook_id= GlobalVars.webhook.id,
                token= GlobalVars.webhook.token,
                username= self.username or "Unknown User (WTF???)",
                avatar_url= self.avatar_url,
                files=Files
        );