import re
from ..Data import GlobalVars
from ..Data.IConfig import plugin_config;
from . import GlobalFuns
from typing import Optional
from nonebot.adapters.onebot.v11 import Message as OneBotMessage, MessageSegment as OneBotMessageSegment
from nonebot.adapters.discord.api import Attachment as DiscordAttachment
from nonebot.log import logger

# Emoji正则表达
EMOJI_PATTERN = re.compile(r'<:(\w+):(\d+)>')

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

    # 用户数据
    userNick: Optional[str];
    userName: str;
    #QQGroup: int | str; #什么时候做多群转发的时候在考虑吧
    
    # 构造函数
    def __init__(self, userName: str, userNick: Optional[str]):
        self.userName = userName;
        self.userNick = userNick;

    # 获取名称
    def get_name(self):
        return f"{self.userNick} ({self.userName})" if self.userNick != None else f"{self.userName}";

    # 发送文字
    async def sendGroup(self, Message: str | OneBotMessage):
        message = f"[{self.get_name()}]:\n{Message}";
        await GlobalVars.OneBotBotObj.send_group_msg(group_id=int(plugin_config.onebot_channel), message=message);
    
    # 发送图片
    async def sendImage(self, imageURL: str):
        image_cq = f"[CQ:image,file={imageURL}]";
        await self.sendGroup(OneBotMessage(image_cq));

    # 发送文件
    async def sendFile(self, fileInfo: DiscordAttachment):
        # Debug日志
        logger.debug(f"Download {fileInfo.filename}...");

        # 获取字节码
        FileBytes, FileStateCode = await GlobalFuns.getFile(fileInfo.url);
        if (FileBytes == None):
            logger.warning(f"Failed to download file (Status Code: {FileStateCode})");
            return;
        
        # 获取nonebot2路径
        file_path = GlobalVars.DOWNLOAD_PATH / fileInfo.filename;

        # 写入文件
        with open(file_path, 'wb') as f:
            f.write(FileBytes);
        
        # 当上传文件时提示是谁发送的内容
        await self.sendGroup(f"上传了文件 ({fileInfo.filename})");

        # 上传文件
        await GlobalVars.OneBotBotObj.upload_group_file(group_id=int(plugin_config.onebot_channel), file=str(file_path.resolve()), name=fileInfo.filename);
