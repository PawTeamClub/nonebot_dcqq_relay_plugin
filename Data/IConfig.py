from nonebot import get_driver, get_plugin_config
from typing import List, Optional
from pydantic import BaseModel, validator

class Config(BaseModel):
  discord_channel: int;
  onebot_channel: int;

  class Config:
      extra = "ignore";

plugin_config = get_plugin_config(Config)