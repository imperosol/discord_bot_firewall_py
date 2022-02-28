from DiscordBot.bot import bot
from ressources.env import BOT_URL


@bot.event
async def on_member_join(member):
    await member.send(
        "Bienvenue sur le serveur Discord des étudiants de l'UTT.\n "
        "Ceci n'étant pas une zone de non droit, vous **devez** vous identifier en cliquant ici "
        f"(**que vous soyez étudiant ou prof**) : {BOT_URL}\n"
        "Vous devez également lire les règles dans le channel `accueil`\n\n"
        "En cas de problème, contactez l'un des administrateurs, visibles en haut à droite.\n"
        "Tapez `@help` dans un channel texte pour voir la liste des commandes.`"
    )
