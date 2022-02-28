import discord

from DiscordBot.aux_files.decorators import admin_command
from DiscordBot.bot import bot, context
from discord.ext import commands


@bot.command(name='delSameRole', aliases=['delDuplicateRole'])
@admin_command()
async def _del_same_role(ctx: context) -> None:
    """
    Delete all duplicates to only keep a set of unique roles.
    """
    # pretty inefficient algorithm. I would be grateful if someone improves it
    role_set = set(ctx.guild.roles)
    for role in role_set:
        same_roles = [r for r in ctx.guild.roles if r == role]
        if len(same_roles) > 1:
            for r in same_roles[1:]:
                await r.delete(reason="Role dupliqué")
    await ctx.message.add_reaction('✅')


@bot.command(name='checkSameRole', aliases=['checkDuplicateRole'])
@admin_command()
async def _check_same_role(ctx: context) -> None:
    """
    Send a message with a list of all roles that have duplicates
    """
    duplicates = [
        role for role in set(ctx.guild.roles) if ctx.guild.roles.count(role) > 1
    ]
    await ctx.send("Les rôles suivants sont dupliqués :\n- " + '\n- '.join(duplicates))


@bot.command(name='giveRole')
@admin_command()
@commands.has_permissions(administrator=True)
async def _give_role(ctx: context, *args) -> None:
    """
    Give a role to a member, given a mention of this user and a mention of the role to give him.
    If the user has already the role, do nothing.

    Example:
    ::
        @giveRole @Dylan Seigler#7891 @Ancien
    """
    if len(args) != 2 and not ctx.message.mentions and not ctx.message.role_mentions:
        await ctx.send(":warning: La syntaxe de cette commande est `@giveRole @membre @role`")
        return
    member: discord.Member = ctx.message.mentions[0]
    role: discord.Role = ctx.message.role_mentions[0]
    await member.add_roles(role)
    await ctx.message.add_reaction("✅")


@bot.command(name='removeRole')
@admin_command()
@commands.has_permissions(administrator=True)
async def _remove_role(ctx: context, *args) -> None:
    """
    Remove a role from a member, given a mention of this user and a mention of the role to remove from him.
    If the user does not have the role, do nothing.

    Example:
    ::
        @removeRole @Dylan Seigler#7891 @Etudiant
    """
    if len(args) != 2 and not ctx.message.mentions and not ctx.message.role_mentions:
        await ctx.send(":warning: La syntaxe de cette commande est `@removeRole @membre @role`")
        return
    member: discord.Member = ctx.message.mentions[0]
    role: discord.Role = ctx.message.role_mentions[0]
    await member.remove_roles(role)
    await ctx.message.add_reaction("✅")


@bot.command(name='kickAll')
@admin_command()
@commands.has_permissions(administrator=True)
async def _kick_all(ctx: context) -> None:
    """
    Kick all non bot and non admins members from the server
    """
    expulsed = 0
    for member in ctx.guild.members:
        if not member.guild_permissions.administrator and not member.bot:
            await member.kick(reason="Commande kickAll")
            expulsed += 1
    await ctx.send(f"Fin de l'opération. {expulsed} personnes ont été éjectées du serveur")


@bot.command(name='removeAllFromRole')
@admin_command()
async def _remove_all_from_role(ctx: context, *args):
    """
    Removes all people from a role. Ensures that no one else has the role. The role still exists afterwards.

    Example:
    ::
        removeAllFromRole @NF04
    """
    if len(args) != 1 and not ctx.message.role_mentions:
        await ctx.send(":warning: Erreur. La syntaxe est `@removeAllFromRole @role`. Le rôle doit exister !")
        return
    role: discord.Role = args[0]
    for member in role.members:
        member.remove_roles(role)
    await ctx.message.add_reaction('✅')


bot_commands = [_check_same_role, _del_same_role, _give_role, _remove_role, _remove_all_from_role, _kick_all]
