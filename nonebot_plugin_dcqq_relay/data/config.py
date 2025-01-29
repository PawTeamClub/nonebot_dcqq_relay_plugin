from typing         import List, Optional
from nonebot        import get_plugin_config
from pydantic       import BaseModel

# 配置类，用于存储多个映射关系
class Config(BaseModel):
    # 指定数据目录
    data_dir: Optional[str] = None

    # 机器人配置
    discord_guild: int    # Discord 服务器 ID
    discord_channel: int  # Discord 频道 ID
    onebot_channel: int   # OneBot 频道 ID

    # 映射关系
    class Config:
        extra = "ignore";

plugin_config = get_plugin_config(Config)
