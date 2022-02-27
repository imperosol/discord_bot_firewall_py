import json

import discord

from DiscordBot.aux_files import utils
from DiscordBot.bot import context, bot
from DiscordBot.aux_files.utils import create_channel, create_category, parse_category
from ressources.paths import UES_PATH
from DiscordBot.aux_files.decorators import admin_command


@bot.command(name='addUe')
@admin_command()
async def _add_ue(ctx: context, *args) -> None:
    """
    discord command to add an UE, given its name, category and channel type.
    if the category doesn't exist, create it.
    The syntax of the command is:
    ::
        @addUE @RoleUE <category> `texte | vocal | lesDeux`
    :param ctx: the discord context of the command
    :param args: the arguments of the command. For the command to be effective, there must be exactly 3 arguments
    :return: None
    """
    if len(args) != 3 or not ctx.message.role_mentions or not args[2].lower() in ("texte", "vocal", "lesdeux"):
        await ctx.send(
            ":warning: Erreur. La syntaxe est `@addUE @RoleUE <category>"
            " texte | vocal | lesDeux`. La catégorie et le rôle doivent déjà exister."
        )
        return
    category = parse_category(ctx.guild, args[1])
    if category is None:
        category = await ctx.guild.create_category(args[1])
    channel_role: discord.Role = ctx.message.role_mentions[0]
    channel_type: int = ('texte', 'vocal', 'lesdeux').index(args[2])
    await create_channel(ctx, channel_role, category, channel_type)
    await ctx.message.add_reaction('✅')


@bot.command(name='addUes')
@admin_command()
async def _add_ues(ctx: context, *args) -> None:
    """
    discord command to add multiple UEs.
    If the category does not exist, create it.
    Create only non-existing channels. No duplicate channels will be created.
    Create the roles associated with the UE channels. No duplicate roles will be created.
    The syntax of the command is:
    ::
        @addUes <branche> `texte | vocal | lesDeux`
    :param ctx: the discord context of the command
    :param args: the arguments of the command. For the command to be effective, there must be exactly 2 arguments
    :return: None
    """
    if len(args) != 1:
        await ctx.send(":warning:  Erreur. La syntaxe est `@addUes <branche> texte | vocal | lesDeux`.")
        return
    with open(UES_PATH, 'r') as f:
        ue_list = json.load(f)[args[0]]
    await create_category(ctx, args[0], ue_list)
    await ctx.message.add_reaction('✅')


@bot.command(name='addAllUes')
@admin_command()
async def _add_all_ues(ctx: context, *args) -> None:
    """
    discord command to create all the UEs channels.
    Create only non-existing channels. No duplicate channels will be created.
    If a category does not exist, create it. No duplicate category will be created.
    Create the roles associated with the UE channels. No duplicate roles will be created.
    The syntax of the command is:
    ::
        @addAllUes

    Please be aware that this command is REALLY heavy in terms of requests to the discord server.
    You must be sure when you use this command, because if you use it multiple times,
    there is a chance that you reach a rate limit
    and that Discord prevents the bot from any operation of role creation for an unknown period of time.
    :param ctx: the discord context of the command
    :param args: the arguments of the command
    :return: None
    """
    if len(args) > 0:
        await ctx.send(":warning:  Erreur. La syntaxe est `@addAllUes`.")
        return
    with open(UES_PATH, 'r') as f:
        ue_dict: dict = json.load(f)
    for category, ue_list in ue_dict.items():
        await create_category(ctx, category, ue_list)
    await ctx.message.add_reaction('✅')


@bot.command(name='delUe')
@admin_command()
async def _del_ue(ctx: context, *args) -> None:
    """
    Discord command to delete an ue channel, given its name.
    Also delete the role associated with the channel.
    If the channel does not exist, send a message to notify the user

    Syntax:
    ::
        @delUe NF04
    :param ctx: the discord context of the command
    :param args: the arguments of the command. For the command to be effective, there must be exactly 1 argument :
        the name of the channel
    """
    if len(args) != 1:
        await ctx.send(":warning:  Erreur. La syntaxe est `@delUe <ue_name>`.")
    channel = utils.parse_channel(ctx.guild, args[0])
    if channel is not None:
        await utils.delete_channel(ctx.guild, channel)
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send(f"Le salon {args[0]} n'existe pas")


@bot.command(name='delUes')
@admin_command()
async def _del_ues(ctx: context, *args) -> None:
    """
    discord command to delete all the UE channels of a category, given the name of this category.
    When all UE channel are deleted, delete the category.
    Also delete the roles associated with each UE channel

    Syntax:
    ::
        @delUes TC
    :param ctx: the discord context of the command
    :param args: the arguments of the command. For the command to be effective, there must be exactly 1 argument :
        the name of the category
    """
    if len(args) != 1:
        await ctx.send(":warning: Erreur. La syntaxe est `@delUEs <category>`.")
        return
    category = parse_category(ctx.guild, args[0])
    if category is None:
        await ctx.send("Cette catégorie n'existe pas.")
        return
    for channel in category.channels:
        await utils.delete_channel(ctx.guild, channel)
    await category.delete(reason="Suppression par un administrateur")
    await ctx.message.add_reaction('✅')


@bot.command(name='delAllUes')
@admin_command()
async def _del_all_ues(ctx: context) -> None:
    """
    discord command to delete all UEs channels of the server.
    When all UE channel are deleted, delete the category.
    Also delete the roles associated with each UE channel

    Syntax:
    ::
        @delAllUes
    :param ctx: the discord context of the command
    """
    ue_categories = 'TC', 'ISI', 'RT', 'GI', 'GM', 'MTE', 'A2I', 'MM', 'ME', 'EC', 'HT', 'PAIP'
    discord_categories = [cat.name for cat in ctx.guild.categories]
    categories = [cat for cat in discord_categories if cat in ue_categories]
    for category in categories:
        await _del_ues(ctx, category)


bot_commands = [_add_ue, _del_ues, _add_ues, _add_all_ues, _del_all_ues, _del_ue]
