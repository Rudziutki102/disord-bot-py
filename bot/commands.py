import discord
from discord.ext import commands


def client_tree_commands_declaration(bot: commands.Bot):
    @bot.tree.command(name='hello')
    async def hello(interaction: discord.Interaction):
        print(interaction)
        await interaction.response.send_message('Hello World', ephemeral=True)
