# Ile kto spędza najwięcej czasu w jakim dniu
# losowe korelacje
from .events import client_event_declaration
from .commands import client_tree_commands_declaration
import discord
import logging
from discord.ext import commands
from config.settings import TOKEN
intents = discord.Intents.default()
intents.voice_states = True
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

bot = commands.Bot(command_prefix='!', intents=intents)
client_event_declaration(bot)
client_tree_commands_declaration(bot)


def run_bot():
    bot.run(TOKEN, log_handler=handler)
