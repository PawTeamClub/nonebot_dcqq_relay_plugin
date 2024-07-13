from typing import Any, List, Optional, Union
from nonebot.log import logger
from nonebot_dcqq_relay_plugin.config import plugin_config;
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager, EMOJI_PATTERN
from nonebot_dcqq_relay_plugin.Core.global_functions import getFile
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.api import Attachment as DiscordAttachment

#=================================================

# Emoji正则表达
def formatImg(content: str):
    # 如果文本空的就返回空文本
    if not content:
        return "";

    # 如果没有符合正则表达式的直接返回文本
    emojis = EMOJI_PATTERN.findall(content)
    if not emojis:
        return content;

    # 局部变量
    segments = []
    last_end = 0

    # 遍历
    for emoji_name, emoji_id in emojis:
        # 找到表情在原文中的位置
        start = content.index(f'<:{emoji_name}:{emoji_id}>', last_end)
        
        # 添加表情前的文本
        if start > last_end:
            segments.append(OneBotMessageSegment.text(content[last_end:start]))

        # 获取表情的 URL
        emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}.png'

        # 添加转换后的表情（使用 CQ 码）
        segments.append(OneBotMessageSegment.image(emoji_url))

        last_end = start + len(f'<:{emoji_name}:{emoji_id}>')

    # 添加最后一个表情后的文本
    if last_end < len(content):
        segments.append(OneBotMessageSegment.text(content[last_end:]))

    # 包装成OneBot消息后返回
    return OneBotMessage(segments);

class QQ():
    
    # 构造函数
    def __init__(self, userName: str, userNick: Optional[str] = None):
        self.userName = userName;
        self.userNick = userNick;

    # 获取名称
    def getName(self) -> str:
        return f"{self.userNick} ({self.userName})" if self.userNick else self.userName;

    # 发送文字
    async def sendGroup(self, Message: Union[str, OneBotMessage]) -> dict[str, Any]:
        message = f"[{self.getName()}]:\n{Message}";
        return await bot_manager.OneBotObj.send_group_msg(group_id=int(plugin_config.onebot_channel), message=message);
    
    # 发送图片
    async def sendImage(self, image_source: Union[str, DiscordAttachment]) -> dict[str, Any]:
        image_url = image_source if isinstance(image_source, str) else image_source.url
        image_segment = OneBotMessageSegment.image(image_url)
        return await self.sendGroup(OneBotMessage(image_segment))

    # 发送文件
    async def sendFile(self, fileInfo: DiscordAttachment) -> Optional[List[dict[str, Any]]]:
        # Debug日志
        logger.debug(f"Download {fileInfo.filename}...");

        # 获取字节码
        FileBytes, FileStateCode = await getFile(fileInfo.url);
        if FileBytes is None:
            logger.warning(f"Failed to download file (Status Code: {FileStateCode})");
            return;
        
        # 获取nonebot2路径
        file_path = bot_manager.DOWNLOAD_PATH / fileInfo.filename;

        results: List[dict[str, Any]] = [];

        try:
            # 写入文件
            file_path.write_bytes(FileBytes);
            
            # 当上传文件时提示是谁发送的内容
            send_result = await self.sendGroup(f"上传了文件 ({fileInfo.filename})");
            if isinstance(send_result, dict):
                results.append(send_result);
            # 上传文件
            upload_result = await bot_manager.OneBotObj.upload_group_file(
                group_id=int(plugin_config.onebot_channel), 
                file=str(file_path.resolve()), 
                name=fileInfo.filename
            );
            if isinstance(upload_result, dict):
                results.append(upload_result);

        finally:
            # 删除文件
            file_path.unlink(missing_ok=True)

        return results
