import sys

import discord

from DiscordBot.aux_files.utils import parse_ue
from DiscordBot.bot import bot


class EtuMember:
    def __init__(self, first_name: str, last_name: str, semester: str, branch: str, is_student: bool):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.semester: str = semester
        self.branch: str = branch
        self.is_student = is_student

    def get_nickname(self) -> str:
        return f"{self.first_name} {self.last_name.upper()} - {self.branch}{self.semester}"


async def etu_to_discord(etu_member: EtuMember, discord_username: str,
                         guild_id: int, etu_name: str, add_roles: list | tuple | set) -> None:
    guild = bot.get_guild(guild_id)
    if guild is None:
        print(f"Aucun serveur ne correspond à l'id {guild_id}", file=sys.stderr)
        return
    discord_member: discord.Member = discord.utils.get(guild.members, name=discord_username)
    if discord_member is not None:
        # rename user
        await discord_member.edit(nick=etu_member.get_nickname(), reason="Connexion depuis le site etu")
        roles = [parse_ue(guild, ue) for ue in add_roles]
        roles.append(parse_ue(guild, 'Ancien'))
        roles.extend([parse_ue(guild, ue) for ue in ('Etudiant', etu_member.branch)])
        roles = [ue for ue in roles if ue is not None]  # remove potential None values
        await discord_member.add_roles(*roles, reason="Connexion depuis le site etu")
