from mongoengine import *
from datetime import datetime, timezone


class User(Document):
    name = StringField(required=True)
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    discord_name = StringField(required=True)
    discord_avatar = URLField(required=True)
    is_online = BooleanField(default=False)
    discord_id = IntField(required=True)
    meta = {'collection': 'bot-users'}


class VoiceActivity(Document):
    user_id = IntField(required=True)
    username = StringField(required=True)
    channel_id = IntField(required=True)
    channel_name = StringField(required=True)
    joined_at = StringField(required=True)
    left_at = StringField(default=None)
    shared_users = ListField(anything=True, default=[])
    session_duration = FloatField(default=0)
    meta = {'collection': 'voice-activity'}
