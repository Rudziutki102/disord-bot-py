import discord
from discord.ext import commands
from discord import app_commands
from config.settings import ALLOWED_ROLES
from database.models import User
import traceback
allowed_roles: list[int] = list(map(int, ALLOWED_ROLES))


def client_tree_commands_declaration(bot: commands.Bot):
    @bot.tree.command(name='track_user')
    @app_commands.describe(discord_user='Select user to add to DB', name="How you want to name the user")
    async def hello(interaction: discord.Interaction, discord_user: discord.Member, name: str):
        if any(role.id in allowed_roles for role in interaction.user.roles):
            user = User(
                name=name,
                discord_name=discord_user.name,
                discord_avatar=discord_user.avatar.url if discord_user.avatar else None,
                is_online=bool(discord_user.voice.channel),
                discord_id=discord_user.id
            )
            try:
                await user.save()
                print(f'User {discord_user} saved to DB')
                await interaction.response.send_message(f'You added {discord_user} as a {name}', ephemeral=True)
            except Exception as e:
                print(f"Error saving user: {e}")
            return
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"Error: {error}")
        traceback.print_exc()
