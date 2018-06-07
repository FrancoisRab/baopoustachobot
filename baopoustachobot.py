import random
import requests
from discord.ext.commands import Bot
from discord import Game

TOKEN = 'NDU0MDE5MTc0NzQ3MDc4NjY3.DfnaVg.rRMcTuWdUMSg5grmMhJ9hvPhumQ'
BOT_PREFIX = ('?', '!')

client = Bot(command_prefix=BOT_PREFIX)



@client.command(pass_context=True,
                aliases=['hi', 'salut', 'hey', 'bonjour'])

async def hello(context):
  possible_responses = [
    "Une journée sans te voir, n'est pas une bonne journée ",
    "Ca me fait chaud au coeur de te voir ici ",
    "Ah ! Bien le bonjour "
  ]

  await client.say(random.choice(possible_responses) + context.message.author.mention)



@client.command()
async def square(number):
  squared_value = int(number) * int(number)
  await client.say(str(number) + ' au carré est égal à : ' + str(squared_value))

@client.event
async def on_ready():
  await client.change_presence(game=Game(name="être le plus beau bot"))
  print("Hop " + client.user.name + " est connecté !")

@client.command()
async def stats(tag):
  url = "https://api.royaleapi.com/player/" + tag
  headers = {
      'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODA2LCJpZGVuIjoiMjAwMjMyMTAyNzUzNDY4NDE2IiwibWQiOnt9LCJ0cyI6MTUyODMyMTg2NzYzOH0.CPCUq-RK0FEDlNdl9XUUwJ2YnnmJvwa4HJRQRue5LvM"
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()
  await client.say("Les stats de " + data['name'] + ": \n" +
                   "- Trophées actuel : " + str(data['trophies']) + "\n" +
                   "- Trophées max : " + str(data["stats"]["maxTrophies"]) + "\n" +
                   "- Arène : " + str(data["arena"]["arenaID"]) + "\n" +
                   "- Ta carte favorite : " + data["stats"]["favoriteCard"]["name"])

  if data["stats"]["totalDonations"] >= 20000:
    await client.say("Tu es un donateur hors pair avec tes " + str(data["stats"]["totalDonations"]) + " dons !")
  elif data["stats"]["totalDonations"] >= 5000:
    await client.say("Tu es un donateur sympatique " + str(data["stats"]["totalDonations"]) + " dons !")
  else:
    await client.say("Bah alors, tu es tout jeune avec tes " + str(data["stats"]["totalDonations"]) + " dons !")

  await client.say("Decklink : " + data["deckLink"])

@client.command()
async def gdc():
  url = "https://api.royaleapi.com/clan/9C2CQYGY/war"
  headers = {
      'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODA2LCJpZGVuIjoiMjAwMjMyMTAyNzUzNDY4NDE2IiwibWQiOnt9LCJ0cyI6MTUyODMyMTg2NzYzOH0.CPCUq-RK0FEDlNdl9XUUwJ2YnnmJvwa4HJRQRue5LvM"
      }
  response = requests.request("GET", url, headers=headers)
  data = response.json()

  teams = data["standings"]
  top = []
  for team in teams:
    top.append(team['name'])

  baopoustache_position = top.index("Baopoustache") + 1

  if data["state"] == "notInWar":
    await client.say("Aucune guerre de clan en cours...")
  elif data["state"] == "collectionDay":
    await client.say("Jour de collection avec " + str(data["clan"]["participants"]) + " participants !")
  else:
    battles = data["clan"]["participants"] - data["clan"]["battlesPlayed"]
    await client.say("Jour de guerre : " + "\n" +
                     "- Participants : " + str(data["clan"]["participants"]) + "\n" +
                     "- " + str(battles) + " joueurs n'ont pas encore fait leur match de guerre" + "\n" +
                     " - Les Baopoustaches sont actuellement : #" + str(baopoustache_position))


client.run(TOKEN)
