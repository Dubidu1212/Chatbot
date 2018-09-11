import logging
import discord
import asyncio
import random
import time
import secrets

#import vote

logging.basicConfig(level=logging.INFO)
client = discord.Client()
finishedSetup = True

###voting
voting = False
N = 2 #number players
votes = [0 for i in range(N)]
AlreadyVoted = [False for i in range(N)]
###

###Cupid
CupidInfoSent = False #if list of people to select has been sent
CupidActive = False #when cupid is active
couple = []#people die together
cupidMessage = "Type the two numbers of your chosen ones seperated by a space please"
###
###Help
helpmessage = ""
with open('../resources/help.txt', 'r') as myfile:
  helpmessage = myfile.read()

###
###Infos
started = False
characters = ["Seer", "Cupid", "Witch", "Hunter", "Priest", "Midwife", "Village bicycle"] #num 0: werewolf, num 8: villager
players = {} #dictionary key: player's id, value: player's number
numToId = {} #dictionary key: player's number, value: player's id
memberDict = {} #key: id, value: member
playerCharacter = [] #index 1: index of character
###
###werewolf voting
WinfoSent = False
Wvoting = False
Wdisc = False #discussing
aWerewolfs = 0 #anzahl wölfe
WvotingList = [False for i in range(aWerewolfs)]#AlreadyVoted of W
Wvotes = [0 for i in range(N)]#people to kill
###
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


async def timer():#eventloop with updates all 1/10 of a second
    global CupidInfoSent
    global CupidActive
    global WinfoSent
    while True:
        if CupidActive and not CupidInfoSent:#Cupid
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],cupidMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(N+1) + ": " +memberDict[player[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            CupidInfoSent = True
        ###################################################################
        elif Wvoting and not WinfoSent:#Werwolfs
            for i in range(aWerewolfs):
                tempMessage = []
                for i in range(N):
                    tempMessage.append(str(N+1) + ": " +memberDict[player[i]].name + "\n")
                s = ''.join(tempMessage)
                await client.send_message(memberDict[Werwolfs[i]],s)
            WinfoSent = True
        await asyncio.sleep(0.1)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

async def countdown(t,times,channel):#t = time // times = repetitions of t // channel = channel on whitch countdown is sent
    for i in range(times):
        await asyncio.sleep(t)
        await client.send_message(channel, str(t*times - i*t) + " seconds left")

async def WMessageRelay(message,sender,Werwolfs):#sends all messages to the werwolfs // sender member which sends the message//message //Werwolfs list of id of werwolfs
    for i in range(len(Werwolfs)):
        if sender.id != Werwolfs[i] :#prevents returning of the message to the sender
            await client.send_message(memberDict[Werwolfs[i]],sender.name + ": " + message)



@client.event
async def on_message(message):
    if(message.author.id == client.user.id):#used so bot doesnt react to own messages
        return
    isPrivate = False
    if(message.channel.name is None):
        isPrivate = True
    if(not isPrivate):#public messages
        ########game
        global channel
        global members
        members = message.server.members #members
        channel = message.channel

        if message.content.lower() == "start" and not started: #if the message is "started and the game isn't started yet, start it
            mes = await distributeCharacters()
            await client.send_message(channel, mes)
            await asyncio.sleep(3)
        ##########
        if(voting):

            if(( len(message.mentions)==1 ) and (not AlreadyVoted[players[message.author.id]])):#stops players from voting twice
                AlreadyVoted[players[message.author.id]] = True
                votes[players[message.raw_mentions[0]]]+=1
    else:#private messages
        global CupidActive
        if(message.content.lower()=="!help"):
            await client.send_message(message.channel,str(helpmessage))
        if(Wdisc):
            for i in range(aWerewolfs):
                Werwolfs=[1,2,3]

                if(message.author.id == Werwolfs[i]):#TODO replace Werwolfs
                    WMessageRelay(message.content,message.author,Werwolfs)

        elif Wvoting:# TODO: voting without mentions
            for i in range(aWerewolfs):
                if(message.author.id == Werwolfs[i]):
                    if isInt(message.content):
                        WvotingList[i] = True;
                        Wvotes[int(message.content)]+=1

                #    if(len(message.mentions)==1):
                #        WvotingList[i]-= 1
                #        Wvotes[players[message.raw_mentions[0]]]+=1


        elif CupidActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[2][0]]:#if is cupid
                couple = message.content.split(" ")#not checked for wrong input
                CupidActive = False

    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)
#####game
async def distributeCharacters():
    started = True
    aMembers = 0

    for a in members:
        aMembers += 1

    occupated = [False for a in range(aMembers)]  # store the characters which are already taken
    playerCharacter = [[] for a in range(aMembers)]
    print(playerCharacter)

    if aMembers < 5:  # there must be at least 5 players
        return "Not enough players"

    global aWerewolfs
    aWerewolfs = int(round(aMembers * 0.3, 0))  # number of werewolfs (30%)
    count = 0

    for a in members:
        if a.id == client.user.id:
            continue
        players[a.id] = count  # assign a number to each player
        numToId[count] = a.id
        memberDict[a.id] = a
        ran = int(random.random() * time.time()) % aMembers  # pick a random role for this player

        while occupated[ran]:  # if this roll is already taken, look for another one
            ran = random.randint(0, aMembers - 1)

        occupated[ran] = True
        privateChannel = client.get_channel(a.id)

        if ran >= 6 + aWerewolfs:
            list(playerCharacter[8]).append(count)
            if privateChannel is None:
                privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Villager")

        elif ran < aWerewolfs:
            list(playerCharacter[0]).append(count)
            if privateChannel is None:
                privateChannel = await client.start_private_message(a)
            await client.send_message(privateChannel, "You're a Werewolf")

        else:
            playerCharacter[ran - aWerewolfs] = [count]
            if ran - aWerewolfs == 1:
                if privateChannel is None:
                    privateChannel = await client.start_private_message(a)
                await client.send_message(privateChannel, "You're Cupid")
            else:
                if privateChannel is None:
                    privateChannel = await client.start_private_message(a)

                await client.send_message(privateChannel, "You're the " + characters[ran - aWerewolfs])

        count += 1
        ####Addition
        global CupidActive
        CupidActive = True

        aWerewolfs = len(playerCharacter[0]);
        ####


    return "Roles distributed"

######

client.loop.create_task(timer())
client.run(secrets.username, secrets.password)
