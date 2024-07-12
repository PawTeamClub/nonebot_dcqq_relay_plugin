from tortoise.models import Model
from tortoise.fields.data import JSONField, DatetimeField, IntField, CharField

class OnebotMessageIndex(Model):
    id = IntField(pk=True)
    onebot_message_id = CharField(max_length=64, index=True)
    message_mapping_id = IntField()

    class Meta:
        table = "onebot_message_index"

class DiscordMessageIndex(Model):
    id = IntField(pk=True)
    discord_message_id = CharField(max_length=64, index=True)
    message_mapping_id = IntField()

    class Meta:
        table = "discord_message_index"

class MessageMapping(Model):
    id = IntField(pk=True)
    onebot_message_id = CharField(max_length=64, null=True, index=True)
    discord_message_id = CharField(max_length=64, null=True, index=True)
    onebot_message_ids = JSONField(null=True)
    discord_message_ids = JSONField(null=True)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        table = "message_mappings"

    async def save(self, *args, **kwargs):
        await super().save(*args, **kwargs)
        
        if self.onebot_message_ids:
            for onebot_id in self.onebot_message_ids:
                await OnebotMessageIndex.get_or_create(
                    onebot_message_id=onebot_id['id'],
                    message_mapping_id=self.id
                )
        
        if self.discord_message_ids:
            for discord_id in self.discord_message_ids:
                await DiscordMessageIndex.get_or_create(
                    discord_message_id=discord_id['id'],
                    message_mapping_id=self.id
                )