import discord
import logging
import secrets
import random
import asyncio
from datetime import datetime

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
        await story_first_night()

        #while something:
        #    story_day()
        #    story_night()


async def distributeCharacters():
    global playerCharacter
    global aRolls
    global aWerewolfs
    started = True
    aMembers = 0

    for a in members:
        aMembers += 1

    occupated = [False for a in range(aMembers - 1)]  # store the characters which are already taken

    if aMembers < 6:  # there must be at least 5 players
        return "Not enough players"

    aWerewolfs = int(round((aMembers - 1) * 0.3, 0))  # number of werewolfs (30%)
    playerCharacter = [[] for a in range(aMembers - aWerewolfs)]
    aRolls = aMembers - aWerewolfs - 1
    count = 0

    for a in members:
        if a.id == client.user.id:
            continue
        players[a.id] = count  # assign a number to each player
        numToId[count] = a.id
        memberDict[a.id] = a
        ran = int(random.random() * datetime.now().microsecond) % (aMembers - 1)  # pick a random role for this player

        while occupated[ran]:  # if this roll is already taken, look for another one
            ran = int(random.random() * datetime.now().microsecond) % (aMembers - 1)

        occupated[ran] = True
        privateChannel = client.get_channel(a.id)

        if ran >= 6 + aWerewolfs:
            if len(playerCharacter[8]) == 0:
                playerCharacter[8] = [count]
            else:
                list(playerCharacter[8]).append(count)

            privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Villager")

        elif ran < aWerewolfs:
            if len(playerCharacter[0]) == 0:
                #print("Creating werewolf list")
                playerCharacter[0] = [count]
            else:
                #print("add werewolf")
                playerCharacter[0].append(count)

            privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Werewolf")

        else:
            #print("add " + str(ran - aWerewolfs))
            playerCharacter[ran - aWerewolfs + 1] = [count]
            if ran - aWerewolfs == 1:
                privateChannel = await client.start_private_message(a)
                await client.send_message(privateChannel, "You're Cupid")
            else:
                privateChannel = await client.start_private_message(a)
                await client.send_message(privateChannel, "You're the " + characters[ran - aWerewolfs])

        count += 1

    return "Roles distributed"

async def story_first_night():
    print(memberDict[numToId[playerCharacter[2][0]]])
    cupid = memberDict[numToId[playerCharacter[2][0]]]

    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)
    await client.send_message(channel, "Cupid, wake up, it's time for love!")
    #await client.start_private_message(channelCupid)
    await client.send_message(cupid, "Choose a little sweet couple, which will have a romantic time together!")
    print("Works so far")
    CupidActive = True

    if aRolls >= 6:
        channelPriest = memberDict[numToId[playerCharacter[5][0]]]
        await client.send_message(channel, "Wake up, Priest, our life-safer!")
        #await client.start_private_message(channelPriest)
        await client.send_message(channelPriest, "Choose someone, who will be blessed for all nights!")
        PriestActive = True
        if aRolls >= 7:
            channelMidwife = memberDict[numToId[playerCharacter[6][0]]]
            await client.send_message(channel, "Some babys are born, they would be cute twins, Midwife.")
            #await client.start_private_message(channelMidwife)
            await client.send_message(channelMidwife, "Look at those sweet villagers, which one do you want to make to twins?")

    story_night()


async def story_night():
    channelWerewolf = memberDict[numToId[playerCharacter[0][0]]]
    channelSeer = memberDict[numToId[playerCharacter[1][0]]]
    channelWitch = memberDict[numToId[playerCharacter[3][0]]]

    for a in range(aWerewolfs - 1):
        channelWerewolf.append(client.get_channel(numToId[playerCharacter[0][a + 1]]))

    await client.send_message(channel, "Be quite, the Seer is having a vision!")
    #await client.start_private_message(channelSeer)
    await client.send_message(channelSeer, "Of which person do you want to know if he or she is a Werewolf?")
    SeerActive = True

    await client.send_message(channel, "Hurry up, I can see the witch just behind this chimney!")
    #await client.start_private_message(channelWitch)
    await client.send_message(channelWitch, "The Person %s is dying, do you want to give him a second chance or maybe even kill someone else as well?", name)
    WitchActive = True

    if aRolls >= 8:
        channelVillageBicycle = memberDict[numToId[playerCharacter[6][0]]]
        await client.send_message(channel, "The Village Bicycle is looking for a new place to stay this night:smirk:")
        #await client.start_private_message(channelVillageBicycle)
        await client.send_message(channelVillageBicycle, "It's getting boring in this, don't you want to look for another one?.smirk:")
        VillageBicycleActive = True


async def story_day():
    deaths = []

    if not deaths:
        await client.send_message(channel, "Let's make a party, nobody has died tonight!")
    elif len(deaths) == 1:
        await client.send_message(channel, "Unfortunately one person has died. The one who had to leave us is %s", memberDict[numToId[deaths[0]]])

client.run(secrets.username, secrets.password)
