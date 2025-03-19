import discord
from discord.ext import commands
from discord import app_commands


def client_tree_commands_declaration(bot: commands.Bot):
    @bot.tree.command(name='track_user')
    @app_commands.describe(discord_user='Select user to add to DB', name="How you want to name the user")
    async def hello(interaction: discord.Interaction, discord_user: discord.Member, name: str):
        print(interaction)
        await interaction.response.send_message(f'You added {discord_user} as a {name}', ephemeral=True)
