from config.settings import CHANNELS_WITHOUT_TRACKING
from database.models import User, VoiceActivity
from datetime import datetime


def client_event_declaration(bot):
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(e)

    @bot.event
    async def on_voice_state_update(member, before, after):
        user: User = User.objects(discord_id=member.id).first()
        if (bool(user)):
            now = datetime.now()
            if (bool(not before.channel and after.channel)):
                voice_activity = VoiceActivity(
                    user_id=user.discord_id,
                    username=user.name,
                    channel_id=after.channel.id,
                    channel_name=after.channel.name,
                    joined_at=now,
                )
                voice_activity.save()
            else:
                current_voice_activity = VoiceActivity.objects(
                    user_id=user.discord_id, left_at=None).first()
                delta = (now - current_voice_activity.joined_at).total_seconds()/60
                current_voice_activity.update(
                    left_at=now,
                    session_duration=round(delta, 2))
