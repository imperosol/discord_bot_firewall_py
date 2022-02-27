import discord
from discord.ext import commands
from ressources.env import BOT_TOKEN
from DiscordBot.commands.channel_management import bot_commands
from DiscordBot.commands.getters import bot_commands
from DiscordBot.commands.role_management import bot_commands
from DiscordBot.bot import bot


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


def start_bot():
    bot.run(BOT_TOKEN)
