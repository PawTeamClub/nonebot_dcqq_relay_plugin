import os, re, shutil, random, string

from typing                 import Union, Tuple, Optional
from pathlib                import Path
from nonebot.log            import logger
from ..data.pattern         import CQ_CODE

def getFileExtension(url):
    """分割文件名和扩展名"""
    _, extension = os.path.splitext(url)
    return extension[1:]

def getPathFolder(path: Union[str, Path]) -> Optional[Path]:
    """
    确保指定的路径存在，如果不存在则创建它。
    """
    try:
        main_path = Path(path) if isinstance(path, str) else path
        if not main_path.exists():
            main_path.mkdir(parents=True, exist_ok=True);
        return main_path
    except Exception as e:
        logger.error(f"创建文件夹失败: {path}. 原因: {e}")
        return None

def generateRandomString(min: int = 6, max: int = 20) -> str:
    """随机生成一个最小和最大的字符串"""
    length = random.randint(min, max)
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def cleanFolder(path: Path):
    """清理文件夹内容"""

    # 确保路径存在
    if not path.exists():
        logger.warning(f"Folder does not exist: {str(path.resolve())}")
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

def extract_cq(type, strraw):
    matches = re.findall(CQ_CODE, strraw)

    for match in matches:
        cq_type, cq_id = match
        if cq_type == type:
            return cq_id

    return None
