from discord import Enum
from mongoengine import *
from datetime import datetime, timezone


class EventType(Enum):
    MUTE = "MUTE"
    UNMUTE = "UNMUTE"
    STREAM_ON = "STREAM_ON"
    STREAM_OFF = "STREAM_OFF"


class User(Document):
    name = StringField(required=True)
    updated_at = DateTimeField(default=datetime.now())
    discord_name = StringField(required=True)
    discord_avatar = URLField(required=True)
    is_online = BooleanField(default=False)
    discord_id = StringField(required=True)
    meta = {'collection': 'bot-users'}


class Channel(Document):
    channel_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    created_at = DateTimeField(required=True)
    last_updated = DateTimeField(default=datetime.now())
    meta = {"collection": 'channels'}


class SessionEvents(Document):
    user_id = StringField(required=True, unique=True)
    channel_id = StringField(required=True)
    eventType = EnumField(EventType, choices=[
                          EventType.MUTE, EventType.UNMUTE, EventType.STREAM_ON, EventType.STREAM_OFF])
    timestamp = datetime.now()
    meta = {"collection": "voice_activity_events"}


class VoiceActivity(Document):
    user_id = StringField(required=True)
    username = StringField(required=True)
    channel_id = StringField(required=True)
    channel_name = StringField(required=True)
    joined_at = DateTimeField(required=True)
    left_at = DateTimeField(default=None)
    session_duration = FloatField(default=0)
    meta = {'collection': 'voice-activity'}
