from config.settings import CHANNELS_WITHOUT_TRACKING


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
        print(f'member: {member}')
        print(f'before: {before.channel}')
        print(f'after: {after}')
        if (after.channel.id in CHANNELS_WITHOUT_TRACKING):
            print(f'User {member} moved to silent-zone')
            return
        if (bool(not before.channel and after.channel)):
            print(f'{member} joined {after.channel}')
        else:
            print(f'{member} left {before.channel}')
