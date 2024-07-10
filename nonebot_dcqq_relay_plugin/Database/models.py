from tortoise.models import Model
from tortoise.fields.data import JSONField, DatetimeField, IntField, CharField

class MessageMapping(Model):
    id = IntField(pk=True)
    onebot_message_id = CharField(max_length=64, null=True, index=True)
    discord_message_id = CharField(max_length=64, null=True, index=True)
    onebot_message_ids = JSONField(null=True)
    discord_message_ids = JSONField(null=True)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        table = "message_mappings"