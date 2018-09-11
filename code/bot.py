import logging
import discord
import asyncio
import random
import secrets
from datetime import datetime

playerCharacter = [] #index 1: index of character

#import vote

logging.basicConfig(level=logging.INFO)
client = discord.Client()
finishedSetup = True

###voting
# TODO: Alle N funktionen initialisiern
voting = False
N = -1#number players
votes = [0 for i in range(N)]
AlreadyVoted = [False for i in range(N)]
###

###Cupid
CupidInfoSent = False #if list of people to select has been sent
CupidActive = False #when cupid is active
couple = []#people die together
cupidMessage = "Type the two numbers of your chosen ones seperated by a space please"
###
###Priest
PriestInfoSent = False
PriestActive = False
blessed = -1 #person who cannot die in the night
PriestMessage = "Type the number of one to bless please"
###
###Midwife
MidwifeInfoSent =False
MidwifeActive = False
twins = []
MidwifeMessage = "Type the two numbers of your chosen ones seperated by a space please"
###
###Vilage Bycicle
BicycleVisit = 0#playerNumber of person visited

###
###Seer
SeerInfoSent = False
SeerActive= False
SeerMessage = "Please type in the number of the person to perform a seeing on"
###
###witch
WitchInfoSent = False
WitchActive = False
WitchMessage = "Please type in the number of the person you want to check if she is a werewolf"

###
###hunter
HunterActive = False
HunterInfoSent = False
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
deathList = [False for i in range(N)]#false if alive true if dead index = PlayerNumber
deaths = []
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
    global playerCharacter
    global PriestActive
    while True:

        if CupidActive and not CupidInfoSent:  #Cupid-------------------------------------------------------------------Cupid
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],cupidMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            CupidInfoSent = True
        ######
        elif PriestActive and not PriestInfoSent:#Priest-------------------------------------------------------------------Priest
            await client.send_message(memberDict[numToId[playerCharacter[5][0]]],PriestMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            PriestInfoSent = True
        elif MidwifeActive and not MidwifeInfoSent:#Midwife------------------------------------------------------------------Midwife
            await client.send_message(memberDict[numToId[playerCharacter[6][0]]],MidwifeMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            MidwifeInfoSent = True
        elif SeerActive and not SeerInfoSent:#Seer------------------------------------------------------------------------Seer
            await client.send_message(memberDict[numToId[playerCharacter[1][0]]],SeerMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            SeerInfoSent = True
        elif HunterActive and not HunterInfoSent:#Hunter-----------------------------------------------------------------Hunter
            await client.send_message(memberDict[numToId[playerCharacter[4][0]]],"PLESE INSERT JAEGERSPRUCH")
            await client.send_message(memberDict[numToId[playerCharacter[4][0]]],"Type the number of the person to kill")
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            HunterInfoSent = True
        elif Wvoting and not WinfoSent:#Werwolfs-------------------------------------------------------------------Werewolfs
            for i in range(aWerewolfs):
                tempMessage = []
                for i in range(N):
                    tempMessage.append(str(i+1) + ": " +memberDict[players[i]].name + "\n")
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

def checkDeath():
    #Lovers
    if deathList[couple[0]]:
        deathList[couple[1]] = True
    elif deathList[couple[1]]:
        deathList[couple[0]] = True
    #Bicycle
    elif deathList[BicycleVisit]:
        deathList[playerCharacter[7][0]] = True
    #Hunter
    elif deathList[playerCharacter[4][0]]:
        HunterActive = True

async def kill(person,unnatural):#person: person to kill in form of PlayerNumber  // unnatural: bool if true killed by witch or werewolf
    if person == blessed and unnatural:#Blessed
        print("Blessed")
    elif person == playerCharacter[7][0]:
        print("Bicycle")
    elif person in twins:#twins
        print("twins")
        if twins.index(person) == 0:
            deathList[twins[1]] = True
        else:
            deathList[twins[0]] = True
    else:
        deathList[person] = True
    checkDeath()
@client.event
async def on_message(message):
    global CupidActive
    global PriestActive
    global MidwifeActive
    global SeerActive
    global HunterActive
    if(message.author.id == client.user.id):#used so bot doesnt react to own messages
        return
    isPrivate = False
    if(message.channel.name is None):
        isPrivate = True
    if(not isPrivate):#public messages
        ########game
        global channel
        global N
        global members
        global couple
        global twins
        global blessed
        members = message.server.members #members
        channel = message.channel

        if message.content.lower() == "start" and not started:  # if the message is "started and the game isn't started yet, start it
            mes = await distributeCharacters()
            await client.send_message(channel, mes)
            if mes == "Not enough players":
                return
            await asyncio.sleep(3)
            await story_first_night()
            x = 0

            while x < 1:
                story_night()
                story_day()
                x = 1
        ##########
        if(voting):

            if(( len(message.mentions)==1 ) and (not AlreadyVoted[players[message.author.id]])):#stops players from voting twice
                AlreadyVoted[players[message.author.id]] = True
                votes[players[message.raw_mentions[0]]]+=1
    else:#private messages

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

                couple = list(map(int,message.content.split(" "))) #not checked for wrong input
                #send message to couple so they know who is their couple
                print(couple)

                for a in range(len(couple)):
                    couple[a] -= 1

                await client.send_message(memberDict[numToId[couple[0]]],"your love is " + memberDict[numToId[couple[1]]].name)
                await client.send_message(memberDict[numToId[couple[1]]],"your love is " + memberDict[numToId[couple[0]]].name)
                CupidActive = False
        elif PriestActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[5][0]]:

                blessed = int(message.content) - 1
                PriestActive = False
        elif MidwifeActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[6][0]]:
                #yolo
                twins = list(map(int,message.content.split(" ")))

                for a in range(len(twins)):
                    twins[a] -= 1

                #send message to twins so they know who is their twins
                await client.send_message(memberDict[numToId[twins[0]]],"your twin is " + memberDict[numToId[twins[1]]].name)
                await client.send_message(memberDict[numToId[twins[1]]],"your twin is " + memberDict[numToId[twins[0]]].name)

                MidwifeActive = False
        elif SeerActive:
            if message.author.id == numToId[playerCharacter[1][0]]:
                temps = "not "
                if message.content in playerCharacter[0]:
                    temps = ""
                await client.send_message(message.channel,memberDict[numToId[int(message.content)]].name + " is " + temps + "a werewolf")
                SeerActive = False
        elif HunterActive:
            if message.author.id == numToId[playerCharacter[4][0]]:
                await kill(int(message.content),False)

    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)
#####game
async def distributeCharacters():
    global N
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
    N = aMembers - 1
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

    ####Addition

    ####
    return "Roles distributed"




######
#####game
async def story_first_night():
    global CupidActive
    global PriestActive
    global MidwifeActive
    cupid = memberDict[numToId[playerCharacter[2][0]]]

    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)
    await client.send_message(channel, "Cupid, wake up, it's time for love!")
    #await client.start_private_message(channelCupid)
    await client.send_message(cupid, "Choose a little sweet couple, which will have a romantic time together!")
    CupidActive = True
    print(aRolls)

    if aRolls >= 6 - aWerewolfs:
        print("Blabla")
        channelPriest = memberDict[numToId[playerCharacter[5][0]]]

        #await asyncio.wait()
        #add loop to wait for completion of Cupid

        await client.send_message(channel, "Wake up, Priest, our life-safer!")
        #await client.start_private_message(channelPriest)
        await client.send_message(channelPriest, "Choose someone, who will be blessed for all nights!")
        PriestActive = True
        if aRolls >= 7 - aWerewolfs:
            channelMidwife = memberDict[numToId[playerCharacter[6][0]]]
            await client.send_message(channel, "Some babys are born, they would be cute twins, Midwife.")
            #await client.start_private_message(channelMidwife)
            await client.send_message(channelMidwife, "Look at those sweet villagers, which one do you want to make to twins?")


async def story_night():
    print("Works so far")
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

    if aRolls >= 8 - aWerewolfs:
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
#####

client.loop.create_task(timer())
client.run(secrets.username, secrets.password)
