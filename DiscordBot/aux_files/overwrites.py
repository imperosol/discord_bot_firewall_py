from discord import Permissions, PermissionOverwrite, Guild
from discord.guild import Role


def ue_channel_perms(guild: Guild, ue_role: Role) -> dict[Role, PermissionOverwrite]:
    """
    create and return a dict usable to overwrite the permissions of an ue text channel
    Example: ::
        @bot.command()
        async def command(ctx, channel_role):
            perms = overwrites.ue_channel_perms(ctx.guild, channel_role)
            channel = await ctx.guild.create_text_channel(channel_name, overwrites=perms)
    :param guild: the discord server in which the channel is to be created
    :param ue_role: the role corresponding to the ue for which the salon is being created
    :return: a dict usable to overwrite the permissions of an ue channel
    """
    text_perms = Permissions.text()
    text_perms.update(manage_messages=False, read_message_history=True, mention_everyone=False, read_messages=True)
    return {
        guild.default_role: PermissionOverwrite.from_pair([], Permissions.all()),
        ue_role: PermissionOverwrite.from_pair(text_perms, [])
    }


def ue_voice_perms(guild: Guild, ue_role: Role) -> dict[Role, PermissionOverwrite]:
    """
    create and return a dict usable to overwrite the permissions of an ue voice channel
    Example: ::
        @bot.command()
        async def command(ctx, channel_role):
            perms = overwrites.ue_voice_perms(ctx.guild, channel_role)
            channel = await ctx.guild.create_voice_channel(channel_name, overwrites=perms)
    :param guild: the discord server in which the channel is to be created
    :param ue_role: the role corresponding to the ue for which the salon is being created
    :return: a dict usable to overwrite the permissions of an ue channel
    """
    voice_perms = Permissions.voice()
    voice_perms.update(priority_speaker=False, move_members=False, mute_members=False, deafen_members=False)
    return {
        guild.default_role: PermissionOverwrite.from_pair([], Permissions.all()),
        ue_role: PermissionOverwrite.from_pair(voice_perms, [])
    }
