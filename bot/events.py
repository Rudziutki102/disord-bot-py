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
    # myślę że rzeczywiście dobrym pomysłem jest przeniesienie tych rzeczy do osobnych funkcji dla czytelności dodatkowo dodamy jeszcze potem eventy taie jak streaming czy mute
    async def on_voice_state_update(member, before, after):
        user: User = User.objects(discord_id=str(member.id)).first()
        if not user:
            return
        if (user):
            now = datetime.now()
            current_voice_activity = VoiceActivity.objects(
                user_id=user.discord_id, left_at=None
            ).first()
            if current_voice_activity:
                delta = (
                    now - current_voice_activity.joined_at).total_seconds()/60
            try:
                if (not before.channel and after.channel):
                    # first join
                    if str(after.channel.id) not in CHANNELS_WITHOUT_TRACKING:
                        voice_activity = VoiceActivity(
                            user_id=str(user.discord_id),
                            username=user.name,
                            channel_id=str(after.channel.id),
                            channel_name=after.channel.name,
                            joined_at=now,
                        )
                        voice_activity.save()
                elif before.channel and not after.channel:
                    # leaves permanently
                    VoiceActivity.objects(user_id=user.discord_id, left_at=None).update_one(
                        set__left_at=now,
                        set__session_duration=round(delta, 2)
                    )
                else:
                    # switching between channels
                    if str(after.channel.id) in CHANNELS_WITHOUT_TRACKING:
                        VoiceActivity.objects(user_id=user.discord_id, left_at=None).update_one(
                            set__left_at=now,
                            set__session_duration=round(delta, 2))
                    else:
                        if current_voice_activity:
                            VoiceActivity.objects(user_id=user.discord_id, left_at=None).update_one(
                                set__left_at=now,
                                set__session_duration=round(delta, 2))
                        voice_activity = VoiceActivity(
                            user_id=str(user.discord_id),
                            username=user.name,
                            channel_id=str(after.channel.id),
                            channel_name=after.channel.name,
                            joined_at=now,
                        )
                        voice_activity.save()
            except Exception as e:
                logger.exception(f'Błąd przy zapisie : {e}')
