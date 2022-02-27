import discord

from DiscordBot.aux_files import overwrites

TEXT = 0
VOICE = 1
BOTH = 2
channel_ret = discord.TextChannel | discord.VoiceChannel | None
channel_in = discord.TextChannel | discord.VoiceChannel


async def create_channel(ctx, channel_role: discord.Role, category = None, channel_type: int = TEXT) -> channel_ret:
    """
    Given a discord context, a discord role corresponding to the ue to which we want to create a channel,
    the category to create the channel in and the channel type (either TEXT, VOICE or BOTH), create
    an ue channel.
    Both role and category must already exist.
    If a channel already exist, do not create a new one.
    Example: ::
        ue = parse_ue(ctx.guild, "GE21")
        cat = parse_category(ctx.guild, "ME")
        if ue is not None and cat is not None:
            create_channel(ctx, ue, cat, TEXT)  # create a text channel for GE21 in the ME category
    :param ctx: the discord context in which this function is called
    :param channel_role: the role to create the channel for
    :param category: the category in which we want to create the channel in
    :param channel_type: the type of channel
    :return: the channel if it has been created, else None
    """
    channel = None
    channel_name: str = channel_role.name
    if discord.utils.get(ctx.guild.channels, name=channel_name) is not None:  # channel already exists
        await ctx.send(f"Le salon {channel_name} existe déjà")
        return None
    if channel_type in (TEXT, BOTH):
        perms = overwrites.ue_channel_perms(ctx.guild, channel_role)
        channel = await ctx.guild.create_text_channel(channel_name, overwrites=perms, category=category)
        await channel.send(f'{channel_role.mention}, votre salon a été créé')
    if channel_type in (VOICE, BOTH):
        perms = overwrites.ue_voice_perms(ctx.guild, channel_role)
        await ctx.guild.create_voice_channel(channel_name, overwrites=perms, category=category)
    return channel


async def delete_channel(guild, channel: channel_in) -> None:
    """
    given an ue channel, delete this channel and the corresponding ue role.
    Example : ::
        channel = discord.utils.get(ctx.guild.channels, "NF04")
        delete_channel(ctx.guild, channel)
    :param guild: the guild to delete the channel from
    :param channel: the channel to delete
    :return: None
    :raise discord.NotFound: if the channel does not exist
    """
    try:
        await channel.delete(reason="Suppression par un administrateur")
    except discord.NotFound:
        raise discord.NotFound
    role = parse_ue(guild, channel.name.upper())
    if role is not None:
        await role.delete(reason="Suppression par un administrateur")


async def create_category(ctx, category_name: str, ues: list[str] = None,
                          channel_type = TEXT) -> discord.CategoryChannel:
    """
    Given a context, a string category_name, a list of string ues and a channel type,
    create (if not already existing) a category with this name and then create in this category
    the ues given in the list. If the ues in the list have no corresponding role, create those roles.
    If no ue list is given, just create an empty category.
    If the category already exists, do not create a new one and create the ues channels in the old category
    Example: ::
        # create an empty category
        cat1 = await create_category(ctx, 'HT')

        # create a TC category with two text channels
        cat2 = await create_category(ctx, 'TC', ['MT01', 'MT02'], TEXT)

        # create two channels without overwriting the previous ones
        cat3 = await create_category(ctx, 'TC', ['CM02', 'CM03'], TEXT)
    :param ctx: the discord context in which this function is called
    :param category_name: a string corresponding to the name of the category
    :param ues: a list of strings which are the name of the ues we want to create in the category
    :param channel_type: the type of channel to create : either TEXT (0), VOICE (1) or BOTH (2).
    All the created channels will be of the specified type. By default, the type is TEXT
    :return: the created category
    """
    if ues is None:
        ues = []
    category = parse_category(ctx.guild, category_name)
    if category is None:
        category: discord.CategoryChannel = await ctx.guild.create_category(category_name)
    for ue_name in ues:
        ue = parse_ue(ctx.guild, ue_name)
        if ue is None:
            ue: discord.Role = await ctx.guild.create_role(name=ue_name)
        channel = parse_channel(ctx.guild, ue_name)
        if channel is None:  # don't create if the channel already exists
            await create_channel(ctx, ue, category, channel_type)
    return category


def parse_category(guild: discord.Guild, category: str) -> discord.CategoryChannel | None:
    """
    Given a string with the name of an ue, find the category in the server corresponding to this category, if exists.
    If no corresponding category is found, return None.
    Example: ::
        @bot.command()
        async def command(ctx, channel_role):
            ue_category = parse_ue(ctx.guild, "ISI")
            if category is not None:  # always check if return value is not None
                await ctx.send("La catégorie ISI existe")
            else:
                await ctx.send("ISI est une machination illuminati, bien sur que ça n'existe pas")
    :param guild: the discord server in which we want to find the category corresponding to the category name
    :param category: a string whose value is the name of the category
    :return: the category corresponding to the ue category if it exists, else None
    """
    if type(category) != discord.CategoryChannel:
        category = discord.utils.get(guild.categories, name=category)
    return category


def parse_ue(guild: discord.Guild, ue: str) -> discord.Role | None:
    """
    Given a string with the name of an ue, find the role in the server corresponding to this ue, if exists.
    If no corresponding role is found, return None.
    Example: ::
        @bot.command()
        async def command(ctx, channel_role):
            role = parse_ue(ctx.guild, "GE21")
            if role is not None:  # always check if return value is not None
                await ctx.send(f"{role.mention}, votre ue est trop bien, keur keur")
    :param guild: the discord server in which we want to find the role corresponding to the ue name
    :param ue: a string whose value is the name of the ue
    :return: the role corresponding to the ue if it exists, else None
    """
    if type(ue) == str:
        return discord.utils.get(guild.roles, name=ue)
    return None


def parse_channel(guild: discord.Guild, channel: str) -> channel_ret:
    """
    Given a string with the name of a channel, find the corresponding channel, if exists.
    If no corresponding channel is found, return None.
    Example: ::
        @bot.command()
        async def command(ctx, channel_role):
            role = parse_channel(ctx.guild, "GE21")
            if role is not None:  # always check if return value is not None
                await ctx.send(f"Le salon de la meilleure UE est {channel.mention}")
    :param guild: the discord server in which we want to find the role corresponding to the ue name
    :param channel: a string with the name of the channel
    :return: the role corresponding to the ue if it exists, else None
    """
    if type(guild) == str:
        return discord.utils.get(guild.channels, name=channel)
    return None
