import discord
from DiscordBot.bot import bot, context
from DiscordBot.aux_files.decorators import admin_command

from ressources.env import INVITATION_LINK, BOT_URL


@bot.command(name='getNb')
@admin_command()
async def _get_nb(ctx: context, *args) -> None:
    """
    Send a Discord message to the same channel where the command was made with the number of
    member having the role specified in the arguments of the command.

    Example:
    ::
        @getNb @GE21
    :param ctx: the discord context in which the command is written
    :param args: one argument : either the id of the role  or a mention of this role
    """
    if len(args) != 1:
        await ctx.send(":warning: Erreur. La syntaxe est `@getNb <@Role | role_id>`")
    role = None
    if args[0].isdigit():
        role = discord.utils.get(ctx.guild.roles, id=role)
    elif ctx.message.role_mentions:
        role = ctx.message.role_mentions[0]
    if role is None:
        await ctx.send(f"Le rôle {args[0]} n'existe pas")
        return
    await ctx.send(f":white_check_mark: Il y a {len(role.members)} utilisateur(s) dans le rôle {role.name}")


@bot.command(name='getRoles')
@admin_command()
async def _get_roles(ctx: context, *args) -> None:
    """
    Given an integer number, send a discord message with all the roles that are held by this number of members.

    Syntax:
    ::
        @getRoles <integer number>
    :param ctx: the discord context of the command
    :param args: the arguments. For the command to be effective, there must be exactly one argument : an integer
    """
    if len(args) != 1:
        await ctx.send(":warning:  Erreur. La syntaxe est `@getRoles NombreDePersonnes`")
        return
    if not args[0].isdigit():
        await ctx.send(":warning: Erreur. L'argument de la fonction `getRoles` doit être un nombre entier")
        return
    nb_people = int(args[0])
    roles = [role.name for role in ctx.guild.roles if len(role.members) == nb_people]
    if len(roles) == 0:
        await ctx.send("Aucun rôle trouvé")
    else:
        await ctx.send(f"{len(roles)} rôles ont {nb_people} membres :\n- " + "\n- ".join(roles))


@bot.command(name='getZeroOne')
@admin_command()
async def _get_zero_one(ctx: context) -> None:
    """
    Send a Discord message with the list of all roles that are held by zero or one member

    Syntax:
    ::
        @getZeroOne
    :param ctx: the discord context of the command
    """
    roles = [role.name for role in ctx.guild.roles if len(role.members) < 2]
    if len(roles) == 0:
        await ctx.send("Aucun rôle trouvé")
    else:
        await ctx.send(f"{len(roles)} rôles ont moins de deux membres :\n- " + "\n- ".join(roles))


@bot.command(name='getUrl')
@admin_command()
async def _get_url(ctx: context) -> None:
    """
    Send a Discord message with the url of the bot and an invitation link.

    :param ctx: the discord context of the command
    """
    await ctx.send(f"URL de connexion (à transmettre) : {BOT_URL}\n\n"
                   f"Le lien d'invitation direct (peu recommandé) : {INVITATION_LINK}")


@bot.command(name='getMemeberRoles')
@admin_command()
async def _get_member_roles(ctx: context, *args) -> None:
    """
    Displays the list of roles of a member, even if the member is not logged in
    (useful for servers > 1000 members)
    
    :param ctx: the discord context of the command
    :param args: the arguments. For the command to be effective, there must be exactly one argument :
        the mention of the member we want to get the roles of
    """
    if len(args) != 1 or not ctx.message.mentions:
        await ctx.send(":warning: La syntaxe de cette commande est `@getMemberRoles @membre`")
        return
    user: discord.Member = ctx.message.mentions[0]
    await ctx.send(f"{user.name} a {len(user.roles)} rôles : " + ', '.join(user.roles))


bot_commands = [_get_nb, _get_zero_one, _get_roles, _get_url, _get_member_roles]

