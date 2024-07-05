import aiohttp
from nonebot.log import logger

async def getFile(weblink :str):
    try:
        # 不知道为什么会导致SSL证书错误，先关着吧
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(weblink) as response:
                if response.status == 200:
                    return await response.read(), response.status;
                else:
                    return None, response.status
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching file: {e}")
        return None, 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None, 0