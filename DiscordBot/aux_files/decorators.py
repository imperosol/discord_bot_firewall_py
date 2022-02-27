from discord.ext import commands
from ressources.env import ADMIN_CHANNEL_ID


def admin_command():
    def predicate(ctx):
        return ctx.channel.id == ADMIN_CHANNEL_ID
    return commands.check(predicate)

