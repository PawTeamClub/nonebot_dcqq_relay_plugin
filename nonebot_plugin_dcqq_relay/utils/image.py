import imageio, json

from apng                           import APNG
from typing                         import Union, Optional
from pathlib                        import Path
from nonebot.log                    import logger
from lottie.parsers.tgs             import parse_tgs
from lottie.exporters.gif           import export_gif

def lottieToGif(
        lottie_path: Union[str, Path],
        output_gif_path: Union[str, Path],
) -> bool:
    """
    将 Lottie JSON 动画文件转换为 GIF 图片

    :param lottie_path: Lottie 动画文件路径
    :param output_gif_path: 输出 GIF 图片路径

    :return: 转换是否成功
    """
    try:
        # 转换为 Path 对象
        if isinstance(lottie_path, str):
            lottie_path = Path(lottie_path)
        if isinstance(output_gif_path, str):
            output_gif_path = Path(output_gif_path)

        # 检查输入文件是否存在
        if not lottie_path.exists():
            raise FileNotFoundError(f"找不到输入文件: {lottie_path}")

        # 确保输出目录存在
        output_gif_path.parent.mkdir(parents=True, exist_ok=True)

        # 读取原始帧率
        with open(lottie_path, 'r', encoding='utf-8') as f:
            lottie_data = json.load(f)
            original_fps = lottie_data.get('fr', 30)  # 获取原始帧率，默认30

        # 读取 Lottie 动画文件
        animation = parse_tgs(str(lottie_path))

        # 导出为 GIF，使用目标帧率
        export_gif(animation, str(output_gif_path), original_fps)
        logger.debug(f"[lottieToGif] 转换成功! 使用帧率: {original_fps} fps")

        return True
    except Exception as e:
        logger.error(f"[lottieToGif] 转换过程中出现错误: {str(e)}")
        return False

def apngToGif(
        apng_path: Union[str, Path],
        output_gif_path: Union[str, Path]
) -> bool:
    """
    将 APNG 图片转换为 GIF 图片

    :param apng_path: APNG 图片路径
    :param output_gif_path: 输出 GIF 图片路径

    :return: 转换是否成功
    """

    try:
        # 转换为 Path 对象
        if isinstance(apng_path, str):
            apng_path = Path(apng_path)
        if isinstance(output_gif_path, str):
            output_gif_path = Path(output_gif_path)

        # 检查输入文件是否存在
        if not apng_path.exists():
            raise FileNotFoundError(f"找不到输入文件: {apng_path}")

        # 确保输出目录存在
        output_gif_path.parent.mkdir(parents=True, exist_ok=True)

        # 读取 APNG 图片
        apng = APNG.open(str(apng_path))

        # 获取图片 FPS
        delays = []
        for png, control in apng.frames:
            # APNG库中delay直接以毫秒为单位
            delay = control.delay
            delays.append(delay)

        # 使用 imageio 转换为 GIF
        reader = imageio.get_reader(str(apng_path))
        writer = imageio.get_writer(str(output_gif_path), format='GIF', duration=delays, loop=0)

        for frame in reader:
            writer.append_data(frame)

        writer.close()
        reader.close()

        logger.debug(f"[apngToGif] 转换成功! 使用帧率: {1000 / delays[0]} fps")
        return True
    except Exception as e:
        logger.error(f"[apngToGif] 转换过程中出现错误: {str(e)}")
        return False
