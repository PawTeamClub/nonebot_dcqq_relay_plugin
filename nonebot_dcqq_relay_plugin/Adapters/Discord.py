import re
from typing import List, Optional
from nonebot.log import logger
from nonebot_dcqq_relay_plugin.config import plugin_config
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager, ENCODED_FACE_PATTERN
from nonebot_dcqq_relay_plugin.Core.global_functions import getFile, getHttpxFile, generate_random_string
from nonebot.adapters.discord.api import File, MessageGet, MessageReference
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

# 解析cq码
def extract_cq(message_type, message_str):
    pattern = r'\[CQ:(\w+),id=(-?\d+).*?\]'
    matches = re.findall(pattern, message_str)

    for match in matches:
        cq_type, cq_id = match
        if cq_type == message_type:
            return cq_id
    return None

#=================================================

class Discord:

    @classmethod
    async def deleteMessage(cls, MessageID: int):
        if not MessageID:
            return;
        
        findDiscordMessage = await bot_manager.DiscordBotObj.get_channel_message(
            channel_id=int(plugin_config.discord_channel),
            message_id=MessageID
        );

        if not findDiscordMessage:
            return;
        
        await bot_manager.DiscordBotObj.delete_message(
            channel_id=int(plugin_config.discord_channel),
            message_id=MessageID
        )

    @classmethod
    async def deleteWebhookMessage(cls, MessageID: int):

        if not MessageID:
            return;
        
        findDiscordMessage = await bot_manager.DiscordBotObj.get_webhook_message(
            webhook_id=bot_manager.webhook_id,
            token=bot_manager.webhook.token,
            message_id=MessageID
        )

        if not findDiscordMessage:
            return;
        
        await bot_manager.DiscordBotObj.delete_webhook_message(
            webhook_id=bot_manager.webhook_id,
            token=bot_manager.webhook.token,
            message_id=MessageID
        )

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
        if segment.type == "image":

            # 有待优化
            file_byte, file_status_code, file_type = await getHttpxFile(segment.data['url'])
            if file_status_code == 200 and "image" in file_type:
                imgtype = ""

                # 不知道这些类型够不够用
                if "gif" in file_type:
                    imgtype = ".gif"
                elif "jpeg" in file_type:
                    imgtype = ".jpg"
                elif "png" in file_type:
                    imgtype = ".png"
                else:
                    logger.error(f"Unknown Image Type [Type: {file_type}]")
                    return None;

                # 在想是传字节码好还是文件好
                file = File(filename=generate_random_string() + imgtype, content=file_byte)
                return await self.sendFile(file)
        elif segment.type == "mface":
            return await self.sendMessage(segment.data['url'])
        elif segment.type == "face":
            emojiURL = f"https://robonyantame.github.io/QQEmojiFiles/Image/{segment.data.get('id')}.gif"
            file_byte, file_status_code = await getFile(emojiURL)
            if file_status_code == 200:
                return await self.sendMessage(emojiURL)
        return None