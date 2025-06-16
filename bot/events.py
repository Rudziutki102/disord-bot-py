from config.settings import CHANNELS_WITHOUT_TRACKING
from database.models import User, VoiceActivity
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


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
        user: User = User.objects(discord_id=str(member.id)).first()
        if (user):
            now = datetime.now()
            if (not before.channel and after.channel):
                try:
                    voice_activity = VoiceActivity(
                        user_id=str(user.discord_id),
                        username=user.name,
                        channel_id=str(after.channel.id),
                        channel_name=after.channel.name,
                        joined_at=now,
                    )
                    voice_activity.save()
                except Exception as e:
                    logger.exception('błąd', e)
            else:
                current_voice_activity = VoiceActivity.objects(
                    user_id=user.discord_id, left_at=None).first()
                delta = (now - current_voice_activity.joined_at).total_seconds()/60
                try:
                    current_voice_activity.update(
                        left_at=now,
                        session_duration=round(delta, 2))
                except Exception as e:
                    logger.exception('błąd', e)
