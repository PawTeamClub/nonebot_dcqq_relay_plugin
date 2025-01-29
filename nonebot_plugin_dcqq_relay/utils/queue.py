import asyncio

from typing                 import Union, Optional
from nonebot.log            import logger
from ..database.models      import QueueMapping

class Queue:
    def __init__(self, maxsize: int = 1000):
        self._queue = asyncio.Queue(maxsize=maxsize)
        self._running = True
        self._cleanup_lock = asyncio.Lock()

    async def put(
        self,
        platform: str,
        group_id: Union[str, int],
        msg_type: str,
        content: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        meg_id: Optional[Union[str, int]] = None,
    ) -> bool:
        try:
            message = await QueueMapping.create(
                platform=platform,
                group_id=str(group_id),
                message_id=str(meg_id) or "null",
                username= "null" if username is None else username,
                avatar_url= "null" if avatar_url is None else avatar_url,
                msg_type=msg_type,
                content=content
            )

            while self._queue.full():
                await asyncio.sleep(0.1)

            await self._queue.put(message)
            return True
        except Exception as e:
            logger.error(f"从队列插入信息发生错误: {e}")
            return False

    async def get(self) -> Optional[QueueMapping]:
        try:
            message = await self._queue.get()
            return message
        except Exception as e:
            logger.error(f"从队列获取信息发生错误 原因: {e}")
            return None

    def size(self):
        if (self._queue is None) or (not self._running) or (self._queue.empty()):
            return 0
        return self._queue.qsize()

    async def cleanup_processed_messages(self) -> bool:
        """清理已处理的消息"""
        async with self._cleanup_lock:
            try:
                await QueueMapping.filter(processed=True).delete()
                logger.info("删除所有已处理的消息")
                return True
            except Exception as e:
                logger.error(f"删除所有已处理的消息发生错误 原因: {e}")
                return False

    async def mark_processed(self, message: QueueMapping) -> bool:
        """标记消息已处理并立即清理"""
        try:
            message.processed = True
            await message.save()
            self._queue.task_done()
            await message.delete()
            return True
        except Exception as e:
            logger.error(f"标记信息错误 原因: {e}")
            return False

    async def recover_unprocessed_messages(self) -> bool:
        """恢复未处理的消息到队列"""
        try:
            unprocessed = await QueueMapping.filter(processed=False).order_by('created_at')
            for message in unprocessed:
                while self._queue.full():
                    await asyncio.sleep(0.1)
                await self._queue.put(message)
            return True
        except Exception as e:
            logger.error(f"恢复队列失败 原因: {e}")
            return False
