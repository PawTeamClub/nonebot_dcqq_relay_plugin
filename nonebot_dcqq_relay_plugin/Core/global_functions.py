import aiohttp, shutil, httpx, random, string
from typing import Union, Tuple, Optional
from pathlib import Path
from nonebot.log import logger

def getPathFolder(path: Union[str, Path]) -> Path:
    """
    确保指定的路径存在，如果不存在则创建它。

    Args:
        path (Union[str, Path]): 要检查或创建的路径。

    Returns:
        Path: 确保存在的路径对象。
    """
    main_path = Path(path) if isinstance(path, str) else path
    if not main_path.exists():
        main_path.mkdir(parents=True, exist_ok=True);
    return main_path

def generate_random_string(min: int = 6, max: int = 20) -> str:
    """随机生成一个最小和最大的字符串"""
    length = random.randint(min, max)  # 随机生成长度在6到20之间
    characters = string.ascii_letters + string.digits  # 包含大小写字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def cleanDownloadFolder(path: Path):
    """
    清理下载文件夹以保证不会给缓存文件暂满
    """
    # 确保下载路径存在
    if not path.exists():
        logger.warning(f"Download folder does not exist: {str(path.resolve())}")
        return

    # 遍历并删除文件夹中的所有内容
    for item in path.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
                logger.debug(f"Deleted file: {item}")
            elif item.is_dir():
                shutil.rmtree(item)
                logger.debug(f"Deleted directory: {item}")
        except Exception as e:
            logger.error(f"Failed to delete {item}. Reason: {e}")

async def getFile(weblink: str) -> Tuple[Optional[bytes], int]:
    """
    异步获取指定URL的文件内容。
    """
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(weblink) as response:
                if response.status == 200:
                    return await response.read(), response.status
                else:
                    logger.warning(f"Failed to fetch file. Status: {response.status}, URL: {weblink}")
                    return None, response.status
    except aiohttp.ClientError as e:
        logger.error(f"Client error when fetching file: {e}", exc_info=True)
        return None, 0
    except Exception as e:
        logger.error(f"Unexpected error when fetching file: {e}", exc_info=True)
        return None, 0
    
async def getHttpxFile(weblink: str) -> Tuple[Optional[bytes], int, Optional[str]]:
    """
    异步获取指定URL的文件内容，并确定文件类型。
    原因: https://github.com/LagrangeDev/Lagrange.Core/issues/315
    """
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(weblink)
            if response.status_code == 200:
                data = response.content
                content_type = response.headers.get('Content-Type', None)
                return data, response.status_code, str(content_type)
            else:
                logger.warning(f"Failed to fetch file. Status: {response.status_code}, URL: {weblink}")
                return None, response.status_code, None
    except httpx.HTTPError as e:
        logger.error(f"Client error when fetching file: {e}", exc_info=True)
        return None, 0, None
    except Exception as e:
        logger.error(f"Unexpected error when fetching file: {e}", exc_info=True)
        return None, 0, None