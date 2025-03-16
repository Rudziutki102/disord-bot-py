# Ile kto spędza najwięcej czasu w jakim dniu
# losowe korelacje
import discord
import logging
from config.settings import TOKEN
intents = discord.Intents.default()
intents.voice_states = True
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_voice_state_update(member,before,after):
    print(f'member: {member}')
    print(f'before: {before.channel}')
    print(f'after: {after}')


def run_bot():
    client.run(TOKEN,log_handler=handler)
    
