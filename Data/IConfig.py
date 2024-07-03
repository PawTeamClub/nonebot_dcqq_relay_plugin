from nonebot import get_driver
from typing import List, Optional
from pydantic import BaseModel

class Config(BaseModel):
  discordChannel: str;
  onebotChannel: str;

global_config = get_driver().config
plugin_config = Config.parse_obj(global_config)