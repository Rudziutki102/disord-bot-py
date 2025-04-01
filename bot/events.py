from config.settings import CHANNELS_WITHOUT_TRACKING
from database.models import User, VoiceActivity
from datetime import datetime


def client_event_declaration(bot):
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        try:
            synced = await bot.tree.sync()
            print(f'commands {len(synced)} commands')
        except Exception as e:
            print(e)

    @bot.event
    async def on_voice_state_update(member, before, after):
        user: User = User.objects(discord_id=member.id).first()
        print(before.channel, after.channel)
        if (bool(user)):
            now = datetime.now()
            if (bool(not before.channel and after.channel)):
                voice_activity = VoiceActivity(
                    user_id=user.discord_id,
                    username=user.name,
                    channel_id=after.channel.id,
                    channel_name=after.channel.name,
                    joined_at=now.strftime('%Y-%m-%d %H:%M:%S'),
                )
                voice_activity.save()
            else:
                current_voice_activity = VoiceActivity.objects(
                    user_id=user.discord_id, left_at=None).first()
                joined_converted = datetime.strptime(
                    current_voice_activity.joined_at, '%Y-%m-%d %H:%M:%S')
                delta = (now - joined_converted).total_seconds()/60
                current_voice_activity.update(
                    left_at=now.strftime('%Y-%m-%d %H:%M:%S'),
                    session_duration=round(delta, 2))
