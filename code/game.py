import discord
import logging
import secrets
import random
import asyncio

logging.basicConfig(level = logging.INFO)
client = discord.Client()

started = False
characters = ["Seer", "Witch", "Cupid", "Hunter", "Midwife", "Priest", "Village bicycle"] #num 0: werewolf, num 8: villager
players = {} #dictionary key: player's id, value: player's number
memberDict = {}
playerCharacter = [] #dictionary key: player's number, value: his character

@client.event
async def on_message(message):
    global channel
    channel = message.channel

    if message.content.lower() == "start" and not started: #if the message is "started and the game isn't
                                                                  # started yet, start it
        distributeCharacters()

def distributeCharacters():
    started = True
    aMembers = 0
    members = discord.Server.members  # all members

    for a in members:
        aMembers += 1

    occupated = [False for a in range(aMembers - 1)]  # store the characters which are already taken
    playerCharacter = [None for a in range(aMembers - 1)]

    if aMembers < 5:  # there must be at least 5 players
        client.send_message(channel, "Not enough players")
        return

    aWerewolfs = int(round(aMembers * 0.3, 0))  # number of werewolfs (30%)
    count = 0

    for a in members:
        players[a.id] = count  # assign a number to each player
        memberDict[a.id] = a
        ran = random.randint(0, aMembers - 1)  # pick a random role for this player

        while occupated[ran]:  # if this roll is already taken, look for another one
            ran = random.randint(0, aMembers - 1)

        occupated[ran] = True

        if ran >= 6 + aWerewolfs:
            list(playerCharacter[8]).append(count)
        elif ran <= aWerewolfs:
            (playerCharacter[0]).append(count)
        else:
            playerCharacter[characters[ran] - aWerewolfs] = ran

        count += 1

def story():
    client.send_message(channel, "It turns night in our small village and all the villagers got to bed")
    asyncio.sleep(3)
    client.send_message(channel, "Cupid, wake up, it's time for love!")

client.run(secrets.username, secrets.password)