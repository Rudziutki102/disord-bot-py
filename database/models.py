from mongoengine import *
import datetime


class User(Document):
    name = StringField(required=True)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    discord_name = StringField(required=True)
    discord_avatar = URLField(required=True)
    is_online = BooleanField(default=False)
    discord_id = IntField(required=True)
    meta = {'collection': 'bot-users'}
