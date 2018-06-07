import random
import requests
import asyncio
import os
from discord.ext.commands import Bot
from discord import Game



# TOKEN = 'TOKEN'
# CR_TOKEN = 'CR_TOKEN'
TOKEN = os.environ['TOKEN']
CR_TOKEN = os.environ['CR_TOKEN']

#TOKEN = 'NDU0MDE5MTc0NzQ3MDc4NjY3.DfnaVg.rRMcTuWdUMSg5grmMhJ9hvPhumQ'
#CR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODA2LCJpZGVuIjoiMjAwMjMyMTAyNzUzNDY4NDE2IiwibWQiOnt9LCJ0cyI6MTUyODMyMTg2NzYzOH0.CPCUq-RK0FEDlNdl9XUUwJ2YnnmJvwa4HJRQRue5LvM"
BOT_PREFIX = ('?', '!')

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
  await client.change_presence(game=Game(name="être le plus beau bot"))
  print("Hop " + client.user.name + " est connecté !")

@client.command(pass_context=True,
                aliases=['hi', 'salut', 'hey', 'bonjour'],
                description="Un peu de politesse ça ne fait de mal à personne")
async def hello(context):
  possible_responses = [
    "Une journée sans te voir, n'est pas une bonne journée ",
    "Ca me fait chaud au coeur de te voir ici ",
    "Ah ! Bien le bonjour "
  ]

  await client.say(random.choice(possible_responses) + context.message.author.mention)

@client.command(description="tape !stats + ID pour obtenir les stats du joueur. ex: !stats 92JV0PL8U")
async def stats(tag):
  url = "https://api.royaleapi.com/player/" + tag
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  await client.say("Les stats de " + data['name'] + ": \n" +
                   "- Trophées actuel : " + str(data['trophies']) + "\n" +
                   "- Trophées max : " + str(data["stats"]["maxTrophies"]) + "\n" +
                   "- Arène : " + str(data["arena"]["arenaID"]) + "\n" +
                   "- Carte favorite : " + data["stats"]["favoriteCard"]["name"])

  if data["stats"]["totalDonations"] >= 20000:
    await client.say("Donateur hors pair avec tes " + str(data["stats"]["totalDonations"]) + " dons !")
  elif data["stats"]["totalDonations"] >= 5000:
    await client.say("Donateur sympatique avec " + str(data["stats"]["totalDonations"]) + " dons !")
  else:
    await client.say("Donateur timide avec " + str(data["stats"]["totalDonations"]) + " dons !")

  await client.say("Decklink : " + data["deckLink"])

@client.command(description="Regarde où en est le clan dans sa guerre en cours, en tapant !gdc")
async def gdc():
  url = "https://api.royaleapi.com/clan/9C2CQYGY/war"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()

  teams = data["standings"]
  top = []
  for team in teams:
    top.append(team['name'])

  baopoustache_position = top.index("Baopoustache") + 1
  bao_in_war = None
  battles = data["clan"]["participants"] - data["clan"]["battlesPlayed"]

  if battles > 1:
    bao_in_war = "- " + str(battles) + " joueurs n'ont pas encore fait leur match de guerre"
  elif battles == 1:
    bao_in_war = "- " + str(battles) + " joueur n'a pas encore fait son match de guerre"
  else:
    bao_in_war = "- Tout le monde a fait son match de guerre ! GG !"

  if data["state"] == "notInWar":
    await client.say("Aucune guerre de clan en cours...")
  elif data["state"] == "collectionDay":
    await client.say("Jour de collection avec " + str(data["clan"]["participants"]) + " participants !")
  else:
    await client.say("Jour de guerre : " + "\n" +
                     "- Participants : " + str(data["clan"]["participants"]) + "\n" +
                     "- Position actuelle : #" + str(baopoustache_position) + "\n" +
                     bao_in_war)

@client.command(description="Plus d'informations sur le clan avec !clan")
async def clan():
  url = "https://api.royaleapi.com/clan/9C2CQYGY"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()

  await client.say('Info sur les Baopoustaches : \n' +
                   "- ID: " + str(data["tag"]) + "\n" +
                   "- Score: " + str(data["score"]) + "\n" +
                   "- Membres: " + str(data["memberCount"]) + "/50 \n" +
                   "- Dons: " + str(data["donations"]))

@client.command(description="Quels seront vos prochains coffres avec !coffres + ID")
async def coffres(tag):
  url = "https://api.royaleapi.com/player/" + tag + "/chests"
  headers = {
      'auth': CR_TOKEN
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()


  await client.say('Les prochains coffres pour cet ID (' + str(tag) + ') :' + '\n' +
                   "- Géant dans : " + str(data["giant"]+1) + " coffres \n" +
                   "- Epic dans : " + str(data["epic"]+1) + " coffres \n" +
                   "- Magique dans : " + str(data["magical"]+1) + " coffres \n" +
                   "- Super Magique: " + str(data["superMagical"]+1) + " coffres \n" +
                   "- Légendaire dans : " + str(data["legendary"]+1) + " coffres")

  upcoming_chests = []

  for chest in data["upcoming"]:
    upcoming_chests.append(chest)


  await client.say("Les 5 prochains coffres sont : \n" +
                   "1 - " + str(upcoming_chests[0].title()) + "\n" +
                   "2 - " + str(upcoming_chests[1].title()) + "\n" +
                   "3 - " + str(upcoming_chests[2].title()) + "\n" +
                   "4 - " + str(upcoming_chests[3].title()) + "\n" +
                   "5 - " + str(upcoming_chests[4].title()))

  # import pdb; pdb.set_trace()

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
