import discord
import logging
import secrets
import random
import asyncio
import time

logging.basicConfig(level = logging.INFO)
client = discord.Client()

started = False
characters = ["Seer", "Cupid", "Witch", "Hunter", "Priest", "Midwife", "Village bicycle"] #num 0: werewolf, num 8: villager
players = {} #dictionary key: player's id, value: player's number
numToId = {} #dictionary key: player's number, value: player's id
memberDict = {} #key: id, value: member
playerCharacter = [] #index 1: index of character

@client.event
async def on_message(message):
    global channel
    global members
    members = message.server.members #members
    channel = message.channel

    if message.content.lower() == "start" and not started: #if the message is "started and the game isn't started yet, start it
        mes = await distributeCharacters()
        await client.send_message(channel, mes)
        if mes == "Not enough players":
            return
        await asyncio.sleep(3)
        await story()


async def distributeCharacters():
    global playerCharacter
    started = True
    aMembers = 0

    for a in members:
        aMembers += 1

    occupated = [False for a in range(aMembers - 1)]  # store the characters which are already taken
    playerCharacter = [[] for a in range(aMembers - 1)]
    print(playerCharacter)

    if aMembers < 6:  # there must be at least 5 players
        return "Not enough players"

    aWerewolfs = int(round((aMembers - 1) * 0.3, 0))  # number of werewolfs (30%)
    count = 0

    for a in members:
        if a.id == client.user.id:
            continue
        players[a.id] = count  # assign a number to each player
        numToId[count] = a.id
        memberDict[a.id] = a
        ran = int(random.random() * time.time()) % (aMembers - 1)  # pick a random role for this player

        while occupated[ran]:  # if this roll is already taken, look for another one
            ran = int(random.random() * time.time()) % (aMembers - 1)

        occupated[ran] = True
        privateChannel = client.get_channel(a.id)

        if ran >= 6 + aWerewolfs:
            if len(playerCharacter[8]) == 0:
                playerCharacter[8] = [count]
            else:
                list(playerCharacter[8]).append(count)

            if privateChannel is None:
                privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Villager")

        elif ran < aWerewolfs:
            if len(playerCharacter[0]) == 0:
                #print("Creating werewolf list")
                playerCharacter[0] = [count]
            else:
                #print("add werewolf")
                playerCharacter[0].append(count)

            if privateChannel is None:
                privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Werewolf")

        else:
            #print("add " + str(ran - aWerewolfs))
            playerCharacter[ran - aWerewolfs + 1] = [count]
            if ran - aWerewolfs == 1:
                if privateChannel is None:
                    privateChannel = await client.start_private_message(a)
                await client.send_message(privateChannel, "You're Cupid")
            else:
                if privateChannel is None:
                    privateChannel = await client.start_private_message(a)

                await client.send_message(privateChannel, "You're the " + characters[ran - aWerewolfs])

        count += 1

    return "Roles distributed"

async def story():
    print(playerCharacter)
    channelCupid = client.get_channel(memberDict[numToId[playerCharacter[2][0]]])

    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)
    await client.send_message(channelCupid, "Cupid, wake up, it's time for love!")
    CupidActive = True


client.run(secrets.username, secrets.password)
