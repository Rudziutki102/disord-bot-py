import os
import discord
from discord.ext import commands
from discord import app_commands
from config.settings import ALLOWED_ROLES
from database.models import User, VoiceActivity
import calendar
import traceback
import xlsxwriter
from database.pipelines import report_pipeline
from datetime import datetime
allowed_roles: list[int] = list(map(int, ALLOWED_ROLES))


def client_tree_commands_declaration(bot: commands.Bot):
    @bot.tree.command(name="generate_report", description="Generates raport for current month, then returns csv")
    async def generate_raport(interaction: discord.Interaction):
        now = datetime.now()
        year = now.year
        month = now.month
        days = calendar.monthrange(year, month)[1]
        start_of_the_month = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        voice_activity = VoiceActivity.objects(
            joined_at__gte=start_of_the_month,
            left_at__ne=None,
            joined_at__lte=now).aggregate(report_pipeline)
        sheet_name = f"{month}_{year}.xlsx"
        workbook = xlsxwriter.Workbook(sheet_name)
        worksheet = workbook.add_worksheet("My Sheet")
        for index, user in enumerate(voice_activity):
            worksheet.write(0, index + 1, user['username'])
            for day in user['days']:
                date_obj = datetime.strptime(day, '%Y-%m-%d')
                day = date_obj.day
                worksheet.write(day, index+1, '1')

        for day in range(1, days):
            worksheet.write(day, 0, day)
        workbook.close()
        try:
            await interaction.response.send_message(f'Raport za {month} {year}, gotowy do pobrania!', file=discord.File(sheet_name))
        finally:
            os.remove(sheet_name)

    @bot.tree.command(name='track_users')
    @app_commands.describe(discord_user='Select user to add to DB', name="How you want to name the user")
    async def hello(interaction: discord.Interaction, discord_user: discord.Member, name: str):
        print(discord_user.voice)
        if any(role.id in allowed_roles for role in interaction.user.roles):
            user = User(
                name=name,
                discord_name=discord_user.name,
                discord_avatar=discord_user.avatar.url if discord_user.avatar else None,
                is_online=bool(
                    discord_user.voice.channel) if discord_user.voice else None,
                discord_id=discord_user.id
            )
            user.save()
            try:
                await interaction.response.send_message(f'You added {discord_user} as a {name}', ephemeral=True)
            except Exception as e:
                print(f"Error saving user: {e}")
            return
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"Error: {error}")
        traceback.print_exc()
