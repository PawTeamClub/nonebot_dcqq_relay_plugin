import json
from typing import List
from pathlib import Path
from tortoise import Tortoise
from .models import MessageMapping
from tortoise.connection import connections

#====================================================================

# Discord数据库

class DiscordModule():
    @classmethod
    async def Create(cls, discord_message_id: str):
        """创建Discord消息表"""
        return await MessageMapping.create(
            discord_message_id=discord_message_id,
            discord_message_ids=json.dumps([]),
            onebot_message_ids=json.dumps([])
        )
    @classmethod
    async def Update(cls, discord_message_id: str, onebot_message_id: str):
        """往Discord表添加QQ信息"""
        mapping = await MessageMapping.get(discord_message_id=discord_message_id)
        mapping.onebot_message_ids.append(onebot_message_id)
        await mapping.save()
    @classmethod
    async def Get(cls, discord_message_id: str) -> List[str]:
        """在Discord表获取QQ消息ID"""
        mapping = await MessageMapping.get_or_none(discord_message_id=discord_message_id)
        return mapping.onebot_message_ids if mapping else []
    @classmethod
    async def Del(cls, discord_message_id: str):
        await MessageMapping.filter(discord_message_id=discord_message_id).delete()

#====================================================================

# QQ数据库

class QQModule():
    @classmethod
    async def Create(cls, onebot_message_id: str):
        """创建QQ消息表"""
        return await MessageMapping.create(
            onebot_message_id=onebot_message_id, 
            discord_message_ids=json.dumps([]),
            onebot_message_ids=json.dumps([])
        )
    @classmethod
    async def Update(cls, onebot_message_id: str, discord_message_id: str):
        """往QQ消息表添加Discord信息"""
        mapping = await MessageMapping.get(onebot_message_id=onebot_message_id)
        mapping.discord_message_ids.append(discord_message_id)
        await mapping.save()
    @classmethod
    async def Get(cls, onebot_message_id: str) -> List[str]:
        """在QQ消息表获取Discord消息ID列表"""
        mapping = await MessageMapping.get_or_none(onebot_message_id=onebot_message_id)
        return mapping.discord_message_ids if mapping else []
    @classmethod
    async def Del(cls, onebot_message_id: str):
        await MessageMapping.filter(onebot_message_id=onebot_message_id).delete()

#====================================================================

# 主数据库方法

class DB():

    # 数据库方法
    dc = DiscordModule();
    qq = QQModule();

    # 初始化数据库
    @classmethod
    async def init(cls, database_path: Path):
        config = {
            "connections": {
                "nonebot_dcqq_relay_db": f"sqlite://{database_path.joinpath('data.sqlite3')}"
            },
            "apps": {
                "nonebot_dcqq_relay": {
                    #"models": ["nonebot_dcqq_relay_plugin.Database.models"],
                    "models": ["Database.models"],
                    "default_connection": "nonebot_dcqq_relay_db",
                }
            },
        }
        await Tortoise.init(config)
        await Tortoise.generate_schemas()

    # 关闭数据库
    @classmethod
    async def close(cls):
        await connections.close_all();

