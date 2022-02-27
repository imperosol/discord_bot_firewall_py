import discord
from discord.ext import commands

context = commands.Context
client = discord.Client()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='@', intents=intents, case_insensitive=True)
