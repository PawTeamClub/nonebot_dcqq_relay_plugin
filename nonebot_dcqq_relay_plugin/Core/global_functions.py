import aiohttp, shutil
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

def cleanDownloadFolder(path: Path):
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

    Args:
        weblink (str): 要获取的文件的URL。

    Returns:
        Tuple[Optional[bytes], int]: 包含文件内容（如果成功）和HTTP状态码的元组。
        如果发生错误，返回 (None, 状态码)。
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