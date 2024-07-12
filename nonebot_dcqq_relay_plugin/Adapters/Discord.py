import re
from typing import List, Optional
from Core.global_functions import getFile
from config import plugin_config
from nonebot.adapters.discord.api import File, MessageGet, MessageReference
from Core.constants import bot_manager, ENCODED_FACE_PATTERN
from nonebot.adapters.onebot.v11 import (
    Bot as OneBotBot,
    MessageSegment as OneBotMessageSegment
)

#=================================================

async def get_user_info(bot: OneBotBot, group_id: int, user_id: int) -> tuple[str, str]:
    user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)
    user_name = f"{user_info['card'] or user_info['nickname']} (QQ: {user_id})"
    avatar_url = f"http://q.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640"
    return user_name, avatar_url

def remove_encoded_faces(text: str) -> str:
    '''移除编码的表情文本'''
    return ENCODED_FACE_PATTERN.sub('', text)


# 解析回复cq码
def extract_reply_cq(message_str):
    reply_pattern = r'\[CQ:reply,id=(-?\d+).*?\]'
    match = re.search(reply_pattern, message_str)
    if match:
        return match.group(1)  # 返回回复的消息 ID
    return None

#=================================================

class Discord:
    def __init__(self, username: str, avatar_url:str):
        self.username = username;
        self.avatar_url = avatar_url;

    @staticmethod
    async def send(message: str) -> MessageGet:
        """Discord -> 发送纯文本(非webhook)"""
        return await bot_manager.DiscordBotObj.send_to(channel_id=int(plugin_config.discord_channel), message=message)

    async def reply(self, message_id: int) -> MessageGet:
        """Discord -> 提醒用户被回复了"""
        return await bot_manager.DiscordBotObj.create_message(
            channel_id=int(plugin_config.discord_channel), 
            message_reference=MessageReference(
                message_id=message_id,
                channel_id=int(plugin_config.discord_channel)
            ), 
            content=f"{self.username} replied to this message!" 
        )

    async def _execute_webhook(self, **kwargs) -> MessageGet:
        """执行webhook的通用方法"""
        return await bot_manager.DiscordBotObj.execute_webhook(
            wait=True,
            webhook_id=bot_manager.webhook.id,
            token=bot_manager.webhook.token,
            username=self.username or "Unknown User",
            avatar_url=self.avatar_url,
            **kwargs
        )

    async def sendMessage(self, message: str) -> Optional[MessageGet]:
        """Discord -> 发送纯文本消息"""
        cleaned_text = remove_encoded_faces(str(message))
        if cleaned_text.strip():  # 只有在清理后的文本不为空时才发送
            return await self._execute_webhook(content=cleaned_text)
        return None

    async def sendFile(self, file: File) -> Optional[MessageGet]:
        """Discord -> 发送单文件"""
        return await self._execute_webhook(files=[file])

    async def sendFiles(self, files: List[File]) -> Optional[MessageGet]:
        """Discord -> 发送多文件"""
        return await self._execute_webhook(files=files)

    async def sendMessageWithFiles(self, message: str, files: List[File]) -> Optional[MessageGet]:
        """Discord -> 发送消息和文件"""
        return await self._execute_webhook(content=message, files=files)

    async def sendFace(self, segment: OneBotMessageSegment) -> Optional[MessageGet]:
        """Discord -> 解析QQ表情后发送"""
        if segment.type in ["image", "mface"]:
            return await self.sendMessage(segment.data['url'])
        elif segment.type == "face":
            emojiURL = f"https://robonyantame.github.io/QQEmojiFiles/Image/{segment.data.get('id')}.gif"
            file_byte, file_status_code = await getFile(emojiURL)
            if file_status_code == 200:
                return await self.sendMessage(emojiURL)
        return None