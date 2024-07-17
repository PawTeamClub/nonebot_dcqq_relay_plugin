import httpx, shutil, random, string, aiohttp, imageio, pyrlottie, numpy

from PIL import Image
from typing import Union, Tuple, Optional
from pathlib import Path
from nonebot.log import logger
from nonebot_dcqq_relay_plugin.Core.constants import bot_manager

def getPathFolder(path: Union[str, Path]) -> Path:
    """
    确保指定的路径存在，如果不存在则创建它。
    """
    main_path = Path(path) if isinstance(path, str) else path
    if not main_path.exists():
        main_path.mkdir(parents=True, exist_ok=True);
    return main_path

def generateRandomString(min: int = 6, max: int = 20) -> str:
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

async def getFile_saveLocal2(weblink: str, fileName: str) -> Tuple[Optional[Path]]:
    """
    获得下载文件的路径
    需要填写网站路径和完整文件名(包括文件后缀)
    **需要一个可辨认的函数名**
    """
    if not weblink:
        logger.error("[getFile_saveLocal2] - Empty Download Link")
        return None

    fileBytes, fileStateCode = await getFile(weblink)
    if not fileBytes:
        logger.error("[getFile_saveLocal2] - Empty Bytes")
        return None

    if not fileName:
        logger.error("[getFile_saveLocal2] - Empty fileName")
    
    file_path = bot_manager.DOWNLOAD_PATH / fileName;

    try:
        file_path.write_bytes(fileBytes)
        return file_path
    except Exception as e:
        logger.error(f"[getFile_saveLocal2] - file_path.write_bytes: {e}")
        return None

async def getFile_saveLocal(weblink: str, fileType: str, fileName: str = generateRandomString()) -> Tuple[Optional[Path], Optional[str]]:
    """
    获得下载文件的路径
    需要填写网站路径和文件类型
    如果fileName不填写，那么就会随机文件名称
    """
    if not weblink:
        logger.error("[getFile_saveLocal2] - Empty Download Link")
        return None

    fileBytes, fileStateCode = await getFile(weblink)
    if not fileBytes:
        logger.error("[getFile_saveLocal] - Empty Bytes")
        return None, None;

    if not fileType:
        logger.error("[getFile_saveLocal] - Empty fileType")
        return None, None;
    
    file_path = bot_manager.DOWNLOAD_PATH / (fileName + f".{fileType}");

    try:
        file_path.write_bytes(fileBytes)
        return file_path, fileName
    except Exception as e:
        logger.error(f"[getFile_saveLocal] - file_path.write_bytes: {e}")
        return None, None

async def apngToGif(apngLink: str) -> Optional[bytes]:

    if not apngLink:
        logger.error("[apngToGif] - Empty apngLink")
        return None

    apng_file, fileName = await getFile_saveLocal(apngLink, "png")
    if not apng_file:
        logger.error("[apngToGif] - Error filePath")
        return None

    gif_file = bot_manager.DOWNLOAD_PATH / (fileName + ".gif");

    try:
        reader = imageio.get_reader(apng_file, format='APNG')
        writer = imageio.get_writer(gif_file, format='GIF', mode='I')

        first_frame = reader.get_data(0)
        width, height = first_frame.shape[1], first_frame.shape[0]

        for frame in reader:
            pil_frame = Image.fromarray(frame)
            background = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            combined = Image.alpha_composite(background, pil_frame)
            rgb_frame = combined.convert("RGB")
            numpy_frame = numpy.array(rgb_frame)
            writer.append_data(numpy_frame)
            background.paste(pil_frame)
        
        writer.close()
        reader.close()
    except Exception as e:
        logger.error(f"[apngToGif] - {e}")
        return None

    gif_bytes = gif_file.read_bytes();
    apng_file.unlink()
    gif_file.unlink()

    return gif_bytes

async def lottieToGif(lottieLink: str) -> Optional[bytes]:

    if not lottieLink:
        logger.error("[apngToGif] - Empty apngLink")
        return None
    
    lottie_file, fileName = await getFile_saveLocal(lottieLink, "json")
    if not lottie_file:
        logger.error("[lottieToGif] - Error filePath")
        return None
    
    gif_file = bot_manager.DOWNLOAD_PATH / (fileName + ".gif");

    try:
        await pyrlottie.convSingleLottie(
            lottieFile=pyrlottie.LottieFile(str(lottie_file.resolve())),
            destFiles={str(gif_file.resolve())}
        )
    except Exception as e:
        logger.error(f"[lottieToGif] - {e}")
        return None
    
    gif_bytes = gif_file.read_bytes();
    lottie_file.unlink()
    gif_file.unlink()

    return gif_bytes