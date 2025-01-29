import re

FACE            = re.compile(r'&#91;([^&#]+)&#93;')                 #QQ Mface Emoji
EMOJI           = re.compile(r'<a?:(\w+):(\d+)>');                  #Discord Emoji
DISCORD_AT      = re.compile(r'<@(\d+)>')

CQ_CODE         = r'\[CQ:(\w+),id=(-?\d+).*?\]'                     #CQ Code
