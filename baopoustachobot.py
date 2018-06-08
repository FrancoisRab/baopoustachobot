import random
import requests
import asyncio
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Game
from database import bdd


TOKEN = os.environ['TOKEN']
CR_TOKEN = os.environ['CR_TOKEN']
BOT_PREFIX = ('?', '!')

bot = Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
  await bot.change_presence(game=Game(name="Clash Royale"))
  print("Hop " + bot.user.name + " est connecté !")

@bot.command(pass_context=True,
             aliases=['hi', 'salut', 'hey', 'bonjour', 'Hello', 'Hi', 'Salut', 'Hey', 'Bonjour'],
             description="Un peu de politesse ça ne fait de mal à personne")
async def hello(context):
  possible_responses = [
    "Une journée sans te voir, n'est pas une bonne journée ",
    "Ca me fait chaud au coeur de te voir ici ",
    "Ah ! Bien le bonjour ",
    "Le plus grand des guerriers est là ! Salut ",
    "Hello ",
    "Bien le bonjour ",
    "Aaaaaaaah, c'est un honneur de te voir ici ",
    "Que serais-je sans toi ",
    "Tout le monde dit bonjour à "
  ]

  await bot.say(random.choice(possible_responses) + context.message.author.mention)

@bot.command(pass_context=True,
             aliases=['Love'],
             description="ex: !love @Pesko pour lui dévoiler vos sentiments")
async def love(ctx, user: discord.Member):
  possible_responses = [
    " tente une approche délicate envers ",
    " met un genoux à terre, et chante sa plus belle sérénade à ",
    " apprécie la présence sur le serveur de ",
    " chuchotte des mots doux à l'oreille de "
  ]
  await bot.say(str(ctx.message.author.mention) + random.choice(possible_responses) + user.mention)


@bot.command(pass_context=True,
             description="Dites au revoir au plus beaux des BOTs !",
             aliases=['Bye', 'Aurevoir', 'aurevoir', 'seeya', 'Seeya'])
async def bye(context):
  possible_responses = [
    "Une bien belle soirée à toi ",
    "A bientôt ",
    "Déjà ? Je ne suis que tristesse... Au revoir ",
    "Reviens vite ",
    "Bye bye ",
    "Je t'attend sagement ici, au revoir ",
    "Ne m'oublie pas et reviens vite "
  ]

  await bot.say(random.choice(possible_responses) + context.message.author.mention)

@bot.command(pass_context=True,
             aliases=['Tag'],
             description="Enregistrer votre ID avec !tag + ID")
async def tag(context, tag):
  #import pdb; pdb.set_trace()
  bdd[str(context.message.author)] = tag
  await bot.say("ID : " + str(tag) + " enregistré sous le pseudo > " + str(context.message.author))
  await bot.say("Dorénavant vous pouvez utiliser !stats et !coffres")


@bot.command(pass_context=True,
             aliases=['Stats'],
             description="tape !stats + ID pour obtenir les stats du joueur. ex: !stats 92JV0PL8U")
async def stats(context):
  url = "https://api.royaleapi.com/player/" + bdd[str(context.message.author)]
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  await bot.say("Les stats de " + data['name'] + ": \n" +
                   "- Trophées actuel : " + str(data['trophies']) + "\n" +
                   "- Trophées max : " + str(data["stats"]["maxTrophies"]) + "\n" +
                   "- Arène : " + str(data["arena"]["arenaID"]) + "\n" +
                   "- Carte favorite : " + data["stats"]["favoriteCard"]["name"])

  if data["stats"]["totalDonations"] >= 20000:
    await bot.say("Donateur hors pair avec tes " + str(data["stats"]["totalDonations"]) + " dons !")
  elif data["stats"]["totalDonations"] >= 5000:
    await bot.say("Donateur sympatique avec " + str(data["stats"]["totalDonations"]) + " dons !")
  else:
    await bot.say("Donateur timide avec " + str(data["stats"]["totalDonations"]) + " dons !")

  await bot.say("Decklink : " + data["deckLink"])

@bot.command(aliases=['Gdc', 'GDC', 'guerre', 'war', 'Guerre', 'War'],
             description="Regarde où en est le clan dans sa guerre en cours, en tapant !gdc")
async def gdc():
  url = "https://api.royaleapi.com/clan/9C2CQYGY/war"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()


  if data["state"] == "notInWar":
    await bot.say("Aucune guerre de clan en cours...")
  elif data["state"] == "collectionDay":
    await bot.say("Jour de collection avec " + str(data["clan"]["participants"]) + " participants !")
  else:
    teams = data["standings"]
    top = []
    for team in teams:
      top.append(team['name'])

    bao_in_war = None
    battles = data["clan"]["participants"] - data["clan"]["battlesPlayed"]

    if battles > 1:
      bao_in_war = "- " + str(battles) + " joueurs n'ont pas encore fait leur match de guerre"
    elif battles == 1:
      bao_in_war = "- " + str(battles) + " joueur n'a pas encore fait son match de guerre"
    else:
      bao_in_war = "- Tout le monde a fait son match de guerre ! GG !"
    baopoustache_position = top.index("Baopoustache") + 1

    await bot.say("Jour de guerre : " + "\n" +
                     "- Participants : " + str(data["clan"]["participants"]) + "\n" +
                     "- Position actuelle : #" + str(baopoustache_position) + "\n" +
                     bao_in_war)

@bot.command(aliases=['Clan'],
             description="Plus d'informations sur le clan avec !clan")
async def clan():
  url = "https://api.royaleapi.com/clan/9C2CQYGY"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()

  await bot.say('Info sur les Baopoustaches : \n' +
                   "- ID: " + str(data["tag"]) + "\n" +
                   "- Score: " + str(data["score"]) + "\n" +
                   "- Membres: " + str(data["memberCount"]) + "/50 \n" +
                   "- Dons: " + str(data["donations"]))

@bot.command(pass_context=True,
             description="Quels seront vos prochains coffres avec !coffres + ID")
async def coffres(context):
  url = "https://api.royaleapi.com/player/" + bdd[str(context.message.author)] + "/chests"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()


  await bot.say('Les prochains coffres pour cet ID (' + bdd[str(context.message.author)] + ') :' + '\n' +
                   "- Géant dans : " + str(data["giant"]+1) + " coffres \n" +
                   "- Epic dans : " + str(data["epic"]+1) + " coffres \n" +
                   "- Magique dans : " + str(data["magical"]+1) + " coffres \n" +
                   "- Super Magique dans : " + str(data["superMagical"]+1) + " coffres \n" +
                   "- Légendaire dans : " + str(data["legendary"]+1) + " coffres")

  upcoming_chests = []

  for chest in data["upcoming"]:
    upcoming_chests.append(chest)


  await bot.say("Les 5 prochains coffres sont : \n" +
                   "1 - " + str(upcoming_chests[0].title()) + "\n" +
                   "2 - " + str(upcoming_chests[1].title()) + "\n" +
                   "3 - " + str(upcoming_chests[2].title()) + "\n" +
                   "4 - " + str(upcoming_chests[3].title()) + "\n" +
                   "5 - " + str(upcoming_chests[4].title()))


bot.remove_command('help')
@bot.command()
async def help(ctx)
  embed = discord.Embed(title="Panneau d'aide du BaopoustachoBot", description="Liste des commandes:", color=0xeee657)

  embed.add_field(name="!tag + ID", value="Permet d'enregistrer ton ID et d'accéder à **!stats** & **!coffres**", inline=False)
  embed.add_field(name="!stats", value="Accédez aux statistiques de votre compte", inline=False)
  embed.add_field(name="!coffres", value="Découvrez vos prochains coffres", inline=False)
  embed.add_field(name="!gdc", value="Où en est le clan dans sa guerre de clan ?", inline=False)
  embed.add_field(name="!clan", value="Accédez aux informations du clan", inline=False)
  embed.add_field(name="!hello", value="Dites moi bonjour, ça fait toujours plaisir !", inline=False)
  embed.add_field(name="!bye", value="Et au revoir aussi...", inline=False)
  embed.add_field(name="!love + @Pseudo", value="Dévoilez vos sentiments à la personne de vos rêves", inline=False)

  await ctx.send(embed=embed)

bot.run(TOKEN)
