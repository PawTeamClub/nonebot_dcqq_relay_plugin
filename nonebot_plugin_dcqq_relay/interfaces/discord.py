from typing import Union, Optional
from ..data.globals import global_vars
from ..data.config import plugin_config
from nonebot.adapters.discord.api import MessageGet

class Discord:
    @classmethod
    async def deleteMessage(cls, MessageID: Union[int, str]) -> bool:
        if (global_vars.discord_bot is None) or (not MessageID):
            return False;

        channel_id      = int(plugin_config.discord_channel)
        message_id      = int(MessageID)

        try:
            findDiscordMessage = await global_vars.discord_bot.get_channel_message(
                channel_id      = channel_id,
                message_id      = message_id
            );

            if (not findDiscordMessage):
                return False;

            await global_vars.discord_bot.delete_message(
                channel_id      = channel_id,
                message_id      = message_id
            )
            return True;
        except Exception as e:
            return False;

    @classmethod
    async def deleteWebhookMessage(cls, MessageID: int) -> bool:
        if (global_vars.discord_bot is None) or (global_vars.webhook is None) or (not MessageID):
            return False;

        id              = global_vars.webhook.id
        token           = global_vars.webhook.token
        message_id      = int(MessageID)

        findDiscordMessage = await global_vars.discord_bot.get_webhook_message(
            token           = token,
            webhook_id      = id,
            message_id      = message_id
        )

        if not findDiscordMessage:
            return False;

        try:
            await global_vars.discord_bot.delete_webhook_message(
                token           = token,
                webhook_id      = id,
                message_id      = message_id
            )
            return True;
        except Exception as e:
            return False;

    @classmethod
    async def sendWebhookMessage(cls, message: str):
        return await cls._execute_webhook(content=message)

    @classmethod
    async def sendMessage(cls, message: str):
        """Discord -> 发送纯文本(非webhook)"""
        if (global_vars.discord_bot is None):
            return;
        return await global_vars.discord_bot.send_to(channel_id=int(plugin_config.discord_channel), message=message)

    @classmethod
    async def _execute_webhook(cls, **kwargs) -> Optional[MessageGet]:
        """执行webhook的通用方法"""
        if (global_vars.discord_bot is None) or (global_vars.webhook is None):
            return None;

        return await global_vars.discord_bot.execute_webhook(
            wait=True,
            webhook_id=global_vars.webhook.id,
            token=global_vars.webhook.token,
            **kwargs
        )
