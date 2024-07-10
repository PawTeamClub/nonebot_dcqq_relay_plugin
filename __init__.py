from nonebot import get_driver
environment = get_driver().config.environment
if environment == "dev":
    from . import nonebot_dcqq_relay_plugin