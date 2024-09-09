import re
from typing import Any, List, Optional, Union, Pattern, Callable
from pathlib import Path
from nonebot.log import logger
from moviepy.editor import VideoFileClip
from nonebot_dcqq_relay_plugin.config import plugin_config;
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager, EMOJI_PATTERN, DISCORD_AT_PATTERN
from nonebot_dcqq_relay_plugin.Core.global_functions import getFile_saveLocal, getFile_saveLocal2
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.api import Attachment as DiscordAttachment

#=================================================

# 这部分代码急需优化

def _format(pattern: Pattern[str], content: str, callbacks: Union[Callable, None] = None):
    if not pattern or not content:
        return ""
    
    check = pattern.findall(content)
    if not check:
        return content
    
    segments = []
    last_end = 0
    
    for match in pattern.finditer(content):
        start, end = match.start(), match.end()
        if start > last_end:
            segments.append(content[last_end:start])
        
        if callable(callbacks):
            func_result = callbacks(match)
            if func_result is not None:
                segments.append(func_result)
        else:
            segments.append(match.group(0))
            
        last_end = end
        
    if last_end < len(content):
        segments.append(content[last_end:])
        
    return segments

async def _async_format(pattern: Pattern[str], content: str, callbacks: Union[Callable, None] = None):
    if not pattern or not content:
        return ""
    
    check = pattern.findall(content)
    if not check:
        return content
    
    segments = []
    last_end = 0
    
    for match in pattern.finditer(content):
        start, end = match.start(), match.end()
        if start > last_end:
            segments.append(content[last_end:start])
        
        if callable(callbacks):
            func_result = await callbacks(match)
            if func_result is not None:
                segments.append(func_result)
        else:
            segments.append(match.group(0))
            
        last_end = end
        
    if last_end < len(content):
        segments.append(content[last_end:])
        
    return segments

#=================================================

# Emoji正则表达
def formatEmoji(content: str):
    # 如果文本空的就返回空文本
    if not content:
        return "";
    
    # 表达替换
    result = _format(EMOJI_PATTERN, content, lambda match: OneBotMessageSegment.image(
        f'https://cdn.discordapp.com/emojis/{match.group(2)}.gif' 
        if match.group(0).startswith('<a:') 
        else f'https://cdn.discordapp.com/emojis/{match.group(2)}.png'
    ))

    # 包装成OneBot消息后返回
    return OneBotMessage(result);

def formatImg(content: str):
    '''
    @todo: 
    此处是处理TODO#4的问题
    但是在想如果UpdateMessagesEvent会修正我是否还要处理这个问题
    因为到时候还要为了处理discord编辑信息的事件
    到时候想想
    '''
    pass;

def formatName(userName: str, userNick: Optional[str], global_name: Optional[str]):
    if userNick:
        return f"{userNick} ({userName})"
    elif global_name:
        return f"{global_name} ({userName})"
    else:
        return userName;

async def formatAT(content: str):
    if not content:
        return ""
    
    content = str(content)
    async def re_format(match):
        user_id = match.group(1)
        user = await bot_manager.DiscordBotObj.get_guild_member(guild_id=int(plugin_config.discord_guild), user_id=int(user_id))
        return f"@{user.user.global_name}({user.user.username})"
        
    result = await _async_format(DISCORD_AT_PATTERN, content, re_format)
    
    return ''.join(result)

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
