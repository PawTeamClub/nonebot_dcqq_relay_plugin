
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    copy: https://github.com/OBKoro1/koro1FileHeader

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                        _oo0oo_
                       o8888888o
                       88" . "88
                       (| -_- |)
                       0\  =  /0
                     ___/`---'\___
                   .' \\|     |// '.
                  / \\|||  :  |||// \
                 / _||||| -:- |||||- \
                |   | \\\  - /// |   |
                | \_|  ''\---/''  |_/ |
                \  .-\__  '-'  ___/-. /
              ___'. .'  /--.--\  `. .'___
           ."" '<  `.___\_<|>_/___.' >' "".
          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
          \  \ `_.   \_ __\ /__ _/   .-` /  /
      =====`-.____`.___ \_____/___.-`___.-'=====
                        `=---='
 
 
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
            佛祖保佑       永不宕机     永无BUG

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from nonebot.plugin import PluginMetadata
from nonebot import get_driver
import sys,os

#===============================================
environment = get_driver().config.environment
if environment == "dev":
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("root path: ", project_root)
    sys.path.insert(0, project_root)
    
#===============================================
    
__plugin_meta__ = PluginMetadata(
    name="nonebot_dcqq_relay_plugin",
    description="使用Nonebot2让Discord和QQ群实现互相通信",
    usage=":<",
    type="application",
    extra={
        "author": "Github@Robonyantame [https://github.com/PawTeamClub]",
        "version": "1.0",
        "priority": 1,
    },
);

#===============================================

from .setup import *
from .Handlers import *

#===============================================

