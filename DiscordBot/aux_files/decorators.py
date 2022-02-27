from discord.ext import commands
from ressources.env import ADMIN_CHANNEL_ID


def admin_command():
    """
    Decorator for a bot command.
    Make the command usable only in the admin channel

    Example:
    ::
        @bot.command()
        @admin_command()
        async def foo(ctx):
            await ctx.send("If you can use this command, it means you are on the admin channel")
    """
    def predicate(ctx):
        return ctx.channel.id == ADMIN_CHANNEL_ID
    return commands.check(predicate)

