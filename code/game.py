import discord
import logging
import secrets
import random
import asyncio

logging.basicConfig(level = logging.INFO)
client = discord.Client()

started = False
characters = ["Seer", "Cupid", "Witch", "Hunter", "Priest", "Midwife", "Village bicycle"] #num 0: werewolf, num 8: villager
players = {} #dictionary key: player's id, value: player's number
numToId = {} #dictionary key: player's number, value: player's
memberDict = {} #key: id, value: member
playerCharacter = [] #index 1: index of character

@client.event
async def on_message(message):
    global channel
    global members
    members = message.server.members #members
    channel = message.channel

    if message.content.lower() == "start" and not started: #if the message is "started and the game isn't started yet, start it
        await client.send_message(channel, distributeCharacters())
        await asyncio.sleep(3)
        await story()


async def distributeCharacters():
    started = True
    aMembers = 0

    for a in members:
        aMembers += 1

    occupated = [False for a in range(aMembers)]  # store the characters which are already taken
    playerCharacter = [[] for a in range(aMembers)]

    if aMembers < 5:  # there must be at least 5 players
        return "Not enough players"

    aWerewolfs = int(round(aMembers * 0.3, 0))  # number of werewolfs (30%)
    count = 0

    for a in members:
        players[a.id] = count  # assign a number to each player
        numToId[count] = a.id
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
            playerCharacter[ran - aWerewolfs] = [count]

        await client.send_message()
        count += 1

    return "Roles distributed"

async def story():
    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)
    client.send_message(somebody, "Cupid, wake up, it's time for love!")
    client.send_message(somebody, "Cupid, wake up, it's time for love!")

client.run(secrets.username, secrets.password)
