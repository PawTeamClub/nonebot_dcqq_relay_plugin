import json
from typing import List, Any, Optional
from .models import MessageMapping, OnebotMessageIndex, DiscordMessageIndex
from pathlib import Path
from tortoise import Tortoise
from nonebot.log import logger
from tortoise.connection import connections
from tortoise.expressions import RawSQL

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
    async def Update(cls, discord_message_id: str, onebot_message_id: str, onebot_message_type: str):
        """往Discord表添加QQ信息"""
        mapping = await MessageMapping.get(discord_message_id=discord_message_id)
        mapping.onebot_message_ids.append({"id": onebot_message_id, "type": onebot_message_type})
        await mapping.save()
    @classmethod
    async def GetTables(cls, discord_message_id: str) -> List[Any]:
        """在Discord表获取QQ消息表"""
        mapping = await MessageMapping.get_or_none(discord_message_id=discord_message_id)
        return mapping.onebot_message_ids if mapping else []
    @classmethod
    async def GetIDs(cls, discord_message_id: str) -> List[Any]:
        """获取Discord表的QQ消息ID"""
        mapping = await cls.GetTables(discord_message_id);
        return [item['id'] for item in mapping] if mapping else []
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
    async def Update(cls, onebot_message_id: str, discord_message_id: str, discord_message_type: str):
        """往QQ消息表添加Discord信息"""
        mapping = await MessageMapping.get(onebot_message_id=onebot_message_id)
        mapping.discord_message_ids.append({"id": discord_message_id, "type": discord_message_type})
        await mapping.save()
    @classmethod
    async def GetTables(cls, onebot_message_id: str) -> List[Any]:
        """在QQ消息表获取Discord消息ID列表"""
        mapping = await MessageMapping.get_or_none(onebot_message_id=onebot_message_id)
        return mapping.discord_message_ids if mapping else []
    @classmethod
    async def GetIDs(cls, onebot_message_id: str) -> List[Any]:
        """获取QQ消息表的QQ消息ID"""
        mapping = await cls.GetTables(onebot_message_id);
        logger.debug(f"mapping len: {len(mapping)}")
        return [item['id'] for item in mapping] if mapping else []
    @classmethod
    async def GetID(cls, onebot_message_id: str, element: Any) -> Optional[Any]:
        """获取与给定元素匹配的单个Discord消息ID"""
        mapping = await cls.GetIDs(onebot_message_id);
        if not mapping:
            return None;
        for segment in mapping:
            if element == segment:
                return segment;
        return None;
    @classmethod
    async def Del(cls, onebot_message_id: str):
        await MessageMapping.filter(onebot_message_id=onebot_message_id).delete()

#====================================================================

# 主数据库方法

class DB():

    @classmethod
    async def init(cls, database_path: Path):
        """初始化数据库"""
        config = {
            "connections": {
                "nonebot_dcqq_relay_db": f"sqlite://{database_path.joinpath('data.sqlite3')}"
            },
            "apps": {
                "nonebot_dcqq_relay": {
                    #"models": ["nonebot_dcqq_relay_plugin.Database.models"],
                    "models": ["nonebot_dcqq_relay_plugin.Database.models"],
                    "default_connection": "nonebot_dcqq_relay_db",
                }
            },
        }
        await Tortoise.init(config)
        await Tortoise.generate_schemas()

    @classmethod
    async def close(cls):
        """关闭数据库"""
        await connections.close_all();

    #======================================================================

    @staticmethod
    async def find_by_onebot_message_id(onebot_message_id: str):
        # 首先查找索引表
        index = await OnebotMessageIndex.filter(onebot_message_id=onebot_message_id).first()
        if index:
            return await MessageMapping.get(id=index.message_mapping_id)

        return None;
    
    @staticmethod
    async def find_by_onebot_message_ids(onebot_message_id: str, page: int = 1, page_size: int = 100):
        offset = (page - 1) * page_size
        query = MessageMapping.filter(
            RawSQL("json_extract(onebot_message_ids, '$[*].id') LIKE ?", [f'%{onebot_message_id}%'])
        )
        total = await query.count()
        results = await query.offset(offset).limit(page_size)
        
        return {
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': results
        }

    @staticmethod
    async def find_by_discord_message_id(discord_message_id: str):
        # 首先查找索引表
        index = await DiscordMessageIndex.filter(discord_message_id=discord_message_id).first()
        
        if index:
            return await MessageMapping.get(id=index.message_mapping_id)

        return None;
    
    @staticmethod
    async def find_by_discord_message_ids(discord_message_id: str, page: int = 1, page_size: int = 100):
        offset = (page - 1) * page_size
        query = MessageMapping.filter(
            RawSQL("json_extract(discord_message_ids, '$[*].id') LIKE ?", [f'%{discord_message_id}%'])
        )
        total = await query.count()
        results = await query.offset(offset).limit(page_size)
        
        return {
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': results
        }