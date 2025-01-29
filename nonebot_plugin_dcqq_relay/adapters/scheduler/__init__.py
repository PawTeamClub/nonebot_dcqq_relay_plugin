from .handler import *
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

messageSendRunning = False

@scheduler.scheduled_job('interval', seconds=1, id='messageSend')
async def messageSendJob():
    """每一秒检测一次消息队列，如果有消息则发送"""
    global messageSendRunning

    # 防止消息发送时再次触发
    if (messageSendRunning is True):
        return

    try:
        messageSendRunning = True
        await messageSend()
    finally:
        messageSendRunning = False
