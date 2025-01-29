import asyncio
from nonebot.log                        import logger
from ...utils.queue                     import Queue
from ...data.globals                    import global_vars
from nonebot.adapters.discord           import Bot as DiscordBot
from nonebot.adapters.onebot.v11        import Bot

async def messageSend():
    """处理消息队列中的多条消息"""

    # 如果全局变量未初始化则直接返回
    if (global_vars.queue is None) or (global_vars.onebot is None) or (global_vars.discord_bot is None):
        return

    # 如果队列为空则直接返回
    if (global_vars.queue.size() == 0):
        return

    # 从队列中获取消息并处理
    while True:
        try:
            message = await global_vars.queue.get()

            # 如果消息为空则直接返回
            if message is None:
                break

            try:
                if message.msg_type == "discord":
                    pass
                elif message.msg_type == "onebot":
                    pass
                await global_vars.queue.mark_processed(message)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue

        except asyncio.QueueEmpty:
            break
        except Exception as e:
            logger.error(f"信息处理中出现意外错误 原因: {e}")
            break

async def send_onebot_message():
    pass

async def send_discord_message():
    pass

async def send_onebot_file():
    pass
