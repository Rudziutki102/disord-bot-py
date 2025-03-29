import discord
from discord.ext import commands
from discord import app_commands
from config.settings import ALLOWED_ROLES
allowed_roles: list[int] = list(map(int, ALLOWED_ROLES))


def client_tree_commands_declaration(bot: commands.Bot):
    @bot.tree.command(name='track_user')
    @app_commands.describe(discord_user='Select user to add to DB', name="How you want to name the user")
    async def hello(interaction: discord.Interaction, discord_user: discord.Member, name: str):
        print(interaction.user.roles)
        if any(role.id in allowed_roles for role in interaction.user.roles):
            await interaction.response.send_message(f'You added {discord_user} as a {name}', ephemeral=True)
            return
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
