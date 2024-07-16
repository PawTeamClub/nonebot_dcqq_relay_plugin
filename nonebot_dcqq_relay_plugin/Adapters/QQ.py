import re
from typing import Any, List, Optional, Union
from pathlib import Path
from nonebot.log import logger
from moviepy.editor import VideoFileClip
from nonebot_dcqq_relay_plugin.config import plugin_config;
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager, EMOJI_PATTERN, DISCORD_AT_PATTERN
from nonebot_dcqq_relay_plugin.Core.global_functions import getFile, getFile_saveLocal, getFile_saveLocal2
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
    for match in EMOJI_PATTERN.finditer(content):
        emoji_full = match.group(0)
        emoji_name = match.group(1)
        emoji_id = match.group(2)
        
        start = match.start()
        end = match.end()

        # 添加表情前的文本
        if start > last_end:
            segments.append(OneBotMessageSegment.text(content[last_end:start]))

        # 判断表情类型并获取相应的 URL
        if emoji_full.startswith('<a:'):
            emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}.gif'
        else:
            emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}.png'

        # 添加转换后的表情（使用 CQ 码）
        segments.append(OneBotMessageSegment.image(emoji_url))

        last_end = end

    # 添加最后一个表情后的文本
    if last_end < len(content):
        segments.append(OneBotMessageSegment.text(content[last_end:]))

    # 包装成OneBot消息后返回
    return OneBotMessage(segments);

def formatName(userName: str, userNick: Optional[str], global_name: Optional[str]):
    if userNick:
        return f"{userNick} ({userName})"
    elif global_name:
        return f"{global_name} ({userName})"
    else:
        return userName;

def formatAT(content: str):
    # 如果文本为空就返回空文本
    if not content:
        return ""

    # 替换函数
    def replace_user_id(match):
        user_id = match.group(1)
        
        # 获取用户信息
        user = bot_manager.DiscordBotObj.get_guild_member(guild_id=int(plugin_config.discord_guild), user_id=int(user_id))
        
        # 返回格式化的用户名
        return f"@{formatName(user.nick, user.user.username, user.user.global_name)}"

    # 使用 re.sub 进行替换
    formatted_content = re.sub(DISCORD_AT_PATTERN, replace_user_id, content)

    return formatted_content

class QQ():
    
    # 构造函数
    def __init__(self, userName: str, globalName: Optional[str], userNick: Optional[str] = None):
        self.Name = formatName(userName, userNick, globalName);

    # 发送文字
    async def sendGroup(self, Message: Union[str, OneBotMessage]) -> dict[str, Any]:
        message = f"[{self.Name}]:\n{Message}";
        return await bot_manager.OneBotObj.send_group_msg(group_id=int(plugin_config.onebot_channel), message=message);
    
    # 发送图片
    async def sendImage(self, image_source: Union[str, DiscordAttachment]) -> dict[str, Any]:
        image_url = image_source if isinstance(image_source, str) else image_source.url
        image_segment = OneBotMessageSegment.image(image_url)
        return await self.sendGroup(OneBotMessage(image_segment))

    # 获得gif文件
    async def getGIFFile(self, embedURL: str) -> Optional[bytes]:    
        try:  
            FilePath, FileName = await getFile_saveLocal(embedURL, "mp4")
            if FilePath is None or FileName is None:
                return None;

            video = VideoFileClip(str(FilePath.resolve()))
            
            # 设置路径
            output_path = bot_manager.DOWNLOAD_PATH / (FileName + ".gif");
            
            # 将视频转换为 GIF
            video.write_gif(str(output_path.resolve()))
            
            # 关闭视频对象
            video.close()

            # 获取GIF字节
            saveGIFBytes = output_path.read_bytes();

            # 刪除文件
            FilePath.unlink()
            output_path.unlink()

            # 返回字节
            return saveGIFBytes

        except Exception as e:
            logger.error(f"Error in getGIFFile: {e}")
            return None

    # 发送文件
    async def sendFile(self, fileInfo: DiscordAttachment) -> Optional[List[dict[str, Any]]]:
        # Debug日志
        logger.debug(f"Download {fileInfo.filename}...");
        
        # 获取字节码
        FilePath = await getFile_saveLocal2(fileInfo.url, fileInfo.filename)
        if FilePath is None:
            logger.error("[sendFile] Failed to download file");
            return;

        results: List[dict[str, Any]] = [];

        try:
            # 当上传文件时提示是谁发送的内容
            send_result = await self.sendGroup(f"上传了文件 ({fileInfo.filename})");
            if isinstance(send_result, dict):
                results.append(send_result);
            # 上传文件
            upload_result = await bot_manager.OneBotObj.upload_group_file(
                group_id=int(plugin_config.onebot_channel), 
                file=str(FilePath.resolve()), 
                name=fileInfo.filename
            );
            if isinstance(upload_result, dict):
                results.append(upload_result);

        finally:
            # 删除文件
            FilePath.unlink(missing_ok=True)

        return results
