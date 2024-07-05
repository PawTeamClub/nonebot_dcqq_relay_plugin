from ..Data import GlobalVars
from ..Data.IConfig import plugin_config;
from . import GlobalFuns
from typing import Optional
from nonebot.adapters.onebot.v11 import Message as OneBotMessage
from nonebot.adapters.discord.api import Attachment as DiscordAttachment
from nonebot.log import logger

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
        await self.sendGroup(f"Upload file ({fileInfo.filename})");

        # 上传文件
        await GlobalVars.OneBotBotObj.upload_group_file(group_id=int(plugin_config.onebot_channel), file=str(file_path.resolve()), name=fileInfo.filename);





