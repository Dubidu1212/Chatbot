import logging
import discord
import asyncio
import random
import secrets
from datetime import datetime

playerCharacter = [] #index 1: index of character
#TODO love yourself

#import vote

logging.basicConfig(level=logging.INFO)
client = discord.Client()
finishedSetup = True

###Cupid
CupidInfoSent = False  # if list of people to select has been sent
CupidActive = False  # when cupid is active
couple = []  # people die together
cupidMessage = "Type the two numbers of your chosen ones seperated by a space."
###
###Priest
PriestInfoSent = False
PriestActive = False
blessed = -1  # person who cannot die in the night
PriestMessage = "Type the number of one to bless."
###
###Midwife
MidwifeInfoSent = False
MidwifeActive = False
twins = []
MidwifeMessage = "Type the two numbers of your chosen ones seperated by a space."
###
###Vilage Bicycle
BicycleVisit = 0  # playerNumber of person visited
BicycleActive = False
BicycleInfoSent = False
BicycleMessage = "Type the number of the person you want to spend your night with"

###
###Seer
SeerInfoSent = False
SeerActive = False
SeerMessage = "Type in the number of the person to perform a seeing on."
###
###witch
WitchInfoSent = False
WitchDoingStuff = False
WitchActive = False
WitchMessage = "Type in the number of the person you want to check if she is a werewolf"
WitchKilling = False #bool
WitchKillingInfoSent = False #bool
###
###hunter
HunterActive = False
HunterShoot = False
HunterInfoSent = False
###
###Help
helpmessage = ""
with open('../resources/help.txt', 'r') as myfile:
    helpmessage = myfile.read()

###
###Infos
N = 0
started = False
characters = ["Seer", "Cupid", "Witch", "Hunter",
 "Priest", "Midwife", "Village Bicycle"]  # num 0: werewolf, num 8: villager
players = {}  # dictionary key: player's id, value: player's number
numToId = {}  # dictionary key: player's number, value: player's id
memberDict = {}  # key: id, value: member

deaths = []
###

###werewolf voting
WinfoSent = False
Wvoting = False
Wdisc = False  # discussing
aWerewolfs = 0  # anzahl wölfe

###

###voting
# TODO: Alle N funktionen initialisiern
voting = False
N = -1#number players

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
    global aWerewolfs
    global Wvoting
    global playerCharacter
    global PriestActive
    global PriestInfoSent
    global MidwifeActive
    global MidwifeInfoSent
    global SeerActive
    global SeerInfoSent
    global BicycleActive
    global BicycleInfoSent
    global HunterActive
    global HunterInfoSent
    global WitchKilling #bool
    global WitchKillingInfoSent #bool
    global WitchActive
    global WitchInfoSent
    global WitchDoingStuff#is active while witch is acting
    global N

    while True:

        if CupidActive and not CupidInfoSent:  #Cupid-------------------------------------------------------------------Cupid
            print("Cupid")
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]], cupidMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[2][0]]],s)
            CupidInfoSent = True
        ######
        elif PriestActive and not PriestInfoSent:#Priest-------------------------------------------------------------------Priest
            print("Priest")
            await client.send_message(memberDict[numToId[playerCharacter[5][0]]], PriestMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[5][0]]],s)
            PriestInfoSent = True
        elif BicycleActive and not BicycleInfoSent:#Bicycle-----------------------------------------------------------Bicycle
            print("Bicycle")
            await client.send_message(memberDict[numToId[playerCharacter[7][0]]],BicycleMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[7][0]]],s)
            BicycleInfoSent=True
        elif MidwifeActive and not MidwifeInfoSent:#Midwife------------------------------------------------------------------Midwife
            print("Midwife")
            await client.send_message(memberDict[numToId[playerCharacter[6][0]]], MidwifeMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[6][0]]],s)
            MidwifeInfoSent = True
        elif SeerActive and not SeerInfoSent:#Seer------------------------------------------------------------------------Seer
            print("Seer")
            await client.send_message(memberDict[numToId[playerCharacter[1][0]]],SeerMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[1][0]]],s)
            SeerInfoSent = True
        elif HunterActive and not HunterInfoSent:#Hunter-----------------------------------------------------------------Hunter
            print("Hunter")
            await client.send_message(memberDict[numToId[playerCharacter[4][0]]],"PLESE INSERT JAEGERSPRUCH")
            await client.send_message(memberDict[numToId[playerCharacter[4][0]]],"Type the number of the person to kill")
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[4][0]]],s)
            HunterInfoSent = True

        elif WitchKilling and not WitchKillingInfoSent:#Witch------------------------------------------------------WitchActive
            await client.send_message(memberDict[numToId[playerCharacter[3][0]]], "Type the number of the one to kill")
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(i+1) + ": " +memberDict[numToId[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacter[3][0]]],s)
            WitchKillingInfoSent = True


        elif Wvoting and not WinfoSent:#Werewolfs-------------------------------------------------------------------Werewolfs
            print("Wvoting")
            for i in range(aWerewolfs):
                tempMessage = []
                for e in range(N):
                    tempMessage.append(str(e+1) + ": " +memberDict[numToId[e]].name + "\n")
                s = ''.join(tempMessage)
                await client.send_message(memberDict[numToId[playerCharacter[0][i]]],s)
            WinfoSent = True
        else:
            pass

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
    return False

async def WerewolfCountdown(t,times):#t = time // times = repetitions of t // channel = channel on whitch countdown is sent
    for i in range(times):
        await asyncio.sleep(t)
        await WMessageRelay( str(t*times - i*t) + " seconds left","Narrator")

    return True

async def WMessageRelay(message,sender):#sends all messages to the werwolfs // sender member which sends the message//message //Werwolfs list of id of werwolfs
    if sender == "Narrator":
        for i in range(len(playerCharacter[0])):
            await client.send_message(memberDict[numToId[playerCharacter[0][i]]],message)
    else:
        for i in range(len(playerCharacter[0])):
            if sender.id != numToId[playerCharacter[0][i]] :#prevents returning of the message to the sender
                await client.send_message(memberDict[numToId[playerCharacter[0][i]]],sender.name + ": " + message)

def checkDeath():

    global HunterShoot
    global HunterActive
    global deathList
    global deaths

    if deathList[couple[0]]:
        deathList[couple[1]] = True
        deaths.append(memberDict[numToId[couple[1]]].name)
    elif deathList[couple[1]]:
        deathList[couple[0]] = True
        deaths.append(memberDict[numToId[couple[0]]].name)
    #Bicycle
    elif deathList[BicycleVisit]:
        deathList[playerCharacter[7][0]] = True
        deaths.append(memberDict[numToId[playerCharacter[7][0]]].name)
    #Hunter
    elif deathList[playerCharacter[4][0]]:
        if not HunterShoot:
            HunterActive = True
            HunterShoot = True

async def kill(person,unnatural):#person: person to kill in form of PlayerNumber  // unnatural: bool if true killed by witch or werewolf
    global deaths
    global deathList
    global aRolls


    if aRolls > 7:
        if person == playerCharacter[7][0]:
            print("Bicycle")
            return
    if person == blessed and unnatural:#Blessed
        print("Blessed")
        return

    elif person in twins:#twins
        print("twins")
        if twins.index(person) == 0:

            deathList[twins[1]] = True
            deaths.append(memberDict[numToId[twins[1]]].name)
        else:
            deathList[twins[0]] = True
            deaths.append(memberDict[numToId[twins[0]]].name)

    else:
        deathList[person] = True
        deaths.append(memberDict[numToId[person]].name)
    checkDeath()
@client.event
async def on_message(message):
    global CupidActive
    global PriestActive
    global MidwifeActive
    global SeerActive
    global HunterActive
    global BicycleActive
    global channel
    global N
    global members
    global couple
    global twins
    global blessed
    global BicycleVisit
    global BicycleInfoSent
    global WvotingList
    global Wvotes
    global Wvoting
    global WitchKilling #bool
    global WitchKillingInfoSent #bool
    global WitchActive
    global WitchDoingStuff
    if(message.author.id == client.user.id):#used so bot doesnt react to own messages
        return
    isPrivate = False
    if(message.channel.name is None):
        isPrivate = True
    if(not isPrivate):#public messages
        ########game

        members = message.server.members #members
        channel = message.channel

        if message.content.lower() == "start" and not started:  # if the message is "started and the game isn't started yet, start it
            mes = await distributeCharacters()
            await client.send_message(channel, mes)
            print(playerCharacter)
            if mes == "Not enough players":
                return
            await asyncio.sleep(3)
            await story_first_night()
            x = 0

            while x < 1:
                await story_night()
                await story_day()
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
            for i in playerCharacter[0]:

                if(message.author.id == numToId[i]):#TODO replace Werwolfs
                    await WMessageRelay(message.content,message.author)

        elif Wvoting:
            for i in range(aWerewolfs):
                if(message.author.id == numToId[playerCharacter[0][i]]):
                    print(playerCharacter[0][i],message.content)
                    if not testNumberOne(message.content):
                        return
                    if WvotingList[i] == True:
                        return
                    WvotingList[i] = True
                    Wvotes[int(message.content)-1]+=1
                    print(Wvotes)

        elif CupidActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[2][0]]:#if is cupid
                if not testNumberpair(message.content):
                    return
                couple = list(map(int,message.content.split(" ")))
                #send message to couple so they know who is their love

                for a in range(len(couple)):
                    couple[a] -= 1

                await client.send_message(memberDict[numToId[couple[0]]],"Your love is " + memberDict[numToId[couple[1]]].name)
                await client.send_message(memberDict[numToId[couple[1]]],"Your love is " + memberDict[numToId[couple[0]]].name)
                await client.send_message(message.channel,"Good choice! I think you'll be invited to the wedding!")
                CupidActive = False
        elif PriestActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[5][0]]:
                if not testNumberOne(message.content):
                    return
                blessed = int(message.content) - 1
                if blessed == players[message.author.id]:
                    await client.send_message(message.channel, "Are you blessing yourself?? Christians should 'Love your neighbor as yourself'!")
                    await client.send_message(message.channel, "Bless someone else!")
                    return

                await client.send_message(message.channel,"Nobody will ever be able to kill this blessed protégé at night!")
                PriestActive = False
        elif MidwifeActive:#perhaps add a time limit
            if message.author.id == numToId[playerCharacter[6][0]]:
                if not testNumberpair(message.content):
                    return
                twins = list(map(int,message.content.split(" ")))

                for a in range(len(twins)):
                    twins[a] -= 1

                #send message to twins so they know who is their twins
                await client.send_message(memberDict[numToId[twins[0]]],"Your twin is " + memberDict[numToId[twins[1]]].name)
                await client.send_message(memberDict[numToId[twins[1]]],"Your twin is " + memberDict[numToId[twins[0]]].name)
                await client.send_message(message.channel,"Look at these beautiful twins. Well done!")
                MidwifeActive = False
        elif SeerActive:
            if message.author.id == numToId[playerCharacter[1][0]]:
                temps = "not "
                if not testNumberOne(message.content):
                    return
                if int(message.content) - 1 in playerCharacter[0]:
                    temps = ""
                await client.send_message(message.channel,memberDict[numToId[int(message.content)-1]].name + " is " + temps + "a werewolf")
                SeerActive = False
        elif HunterActive:
            if message.author.id == numToId[playerCharacter[4][0]]:
                if not testNumberOne(message.content):
                    return
                await client.send_message(message.channel, "With your last breath you shoot through %s's heart", memberDict[numToId[int(message.content)]].name)
                await kill(int(int(message.content) - 1),False)
                HunterActive = False
        elif BicycleActive:
            if message.author.id == numToId[playerCharacter[7][0]]:
                if not testNumberOne(message.content):
                    return
                BicycleVisit = int(message.content) - 1
                await client.send_message(message.channel,":smirk:")
                BicycleActive = False
        elif WitchActive:
            if message.author.id == numToId[playerCharacter[3][0]]:
                # TODO: Check if input is char-----------------------------------------------------------------------------------------------------------------------
                #thumbsdown
                if ord(message.content)!=128078:
                    #thumbsup
                    if ord(message.content)!=128077:
                        #fist
                        if  ord(message.content)!=9994:
                            await client.send_message(message.channel, "Are you trying to kid me?? You have to answer with :-1:,:+1: or :fist:!")
                        else:
                            WitchActive = False

                            await client.send_message(message.channel, "You don't feel pity for this poor dude? You're such a witch!")
                            WitchDoingStuff = False
                    else:
                        await client.send_message(message.channel, "Ooh you're healing, that's very kind! Maybe this this dude is your secret love?:smirk:")
                        # TODO: remove the person from deathList if is in love remove love too
                        WitchActive = False

                        WitchDoingStuff = False # TODO: Paste this on the end of healing
                else:#thumb is down
                    await client.send_message(message.channel,"Feeling like killing someone, are you?:skull:")
                    # TODO: doing killing stuff
                    WitchKilling = True
                    WitchActive = False
        elif WitchKilling:
            # TODO: check input
            if message.author.id == numToId[playerCharacter[3][0]]:
                await kill(int(message.content)-1,True)
                await client.send_message(message.channel,"The job is done")
                WitchDoingStuff = False
    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)
#####game
async def distributeCharacters():
    global N
    global playerCharacter
    global aRolls
    global aWerewolfs
    global deathList
    global WvotingList
    global Wvotes
    global votes
    global AlreadyVoted

    global started

    started = True
    aMembers = 0

    for a in members:
        if not isOnline(a):
            continue
        aMembers += 1

    if aMembers < 6:  # there must be at least 5 players
        started = False
        return "Not enough players"

    aWerewolfs = int(round((aMembers - 1) * 0.3))  # number of werewolfs (30%)

    aRolls = aMembers - aWerewolfs

    if aRolls > 9:
        aRolls = 9

    playerCharacter = [[] for a in range(aRolls)]
    occupated = [False for a in range(aMembers - 1)]  # store the characters which are already taken

    N = aMembers - 1
    #####setup lists
    deathList = [False for i in range(N)]  # false if alive true if dead index = PlayerNumber

    WvotingList = [False for i in range(aWerewolfs)]  # AlreadyVoted of W
    Wvotes = [0 for i in range(N)]  # people to kill

    votes = [0 for i in range(N)]
    AlreadyVoted = [False for i in range(N)]
    #######



    count = 0

    for a in members:
        if not isOnline(a):
            continue

        if a.id == client.user.id:
            continue
        players[a.id] = count  # assign a number to each player
        numToId[count] = a.id
        memberDict[a.id] = a
        ran = int(random.random() * datetime.now().microsecond) % (aMembers - 1)  # pick a random role for this player

        while occupated[ran]:  # if this roll is already taken, look for another one
            ran = int(random.random() * datetime.now().microsecond) % (aMembers - 1)

        occupated[ran] = True

        if ran >= 7 + aWerewolfs:
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
    global aRolls
    global aVillager
    global aWerewolfs
    cupid = memberDict[numToId[playerCharacter[2][0]]]

    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)
    await client.send_message(channel, "Cupid, wake up, it's time for love!")
    #await client.start_private_message(channelCupid)
    await client.send_message(cupid, "Choose a little sweet couple, which will have a romantic time together!")
    CupidActive = True
    if aRolls >= 6:
        channelPriest = memberDict[numToId[playerCharacter[5][0]]]

        #await asyncio.wait()
        while CupidActive:
            await asyncio.sleep(0.1)

        await client.send_message(channel, "Wake up, Priest, our life-safer!")
        #await client.start_private_message(channelPriest)
        await client.send_message(channelPriest, "Choose someone, who will be blessed for all nights!")
        PriestActive = True

        if aRolls >= 7 - aWerewolfs:
            channelMidwife = memberDict[numToId[playerCharacter[6][0]]]

            while PriestActive:
                await asyncio.sleep(0.1)

            await client.send_message(channel, "Some babys are born, they would be cute twins, Midwife.")
            #await client.start_private_message(channelMidwife)
            await client.send_message(channelMidwife, "Look at those sweet villagers, which one do you want to make to twins?")
            MidwifeActive = True

            while MidwifeActive:
                await asyncio.sleep(0.1)
        else:
            while PriestActive:
                await asyncio.sleep(0.1)
    else:
        while CupidActive:
            await asyncio.sleep(0.1)


async def story_night():
    global BicycleActive
    global SeerActive
    global WitchActive
    global Wvoting
    global Wdisc
    global Wvotes
    global WitchDoingStuff
    global name

    channelSeer = memberDict[numToId[playerCharacter[1][0]]]
    channelWitch = memberDict[numToId[playerCharacter[3][0]]]


    if aRolls >= 8:
        channelVillageBicycle = memberDict[numToId[playerCharacter[7][0]]]
        await client.send_message(channel, "The Village Bicycle is looking for a new place to stay this night:smirk:")
        #await client.start_private_message(channelVillageBicycle)
        await client.send_message(channelVillageBicycle, "It's getting boring in this, don't you want to look for another one?:smirk:")
        BicycleActive = True #TODO not working, make it

        while BicycleActive:
            await asyncio.sleep(0.1)

    await client.send_message(channel, "I suppose it would be better if you stay at home, **the Werewolfs are coming!**")

    for werewolf in playerCharacter[0]:
        await client.send_message(memberDict[numToId[werewolf]], "It smells of human flesh here, aren't you getting hungry?:yum:")

    Wdisc = True
    for werewolf in playerCharacter[0]:
        await client.send_message(memberDict[numToId[werewolf]], "You've got 30 seconds to discuss your prey")
    while not await WerewolfCountdown(1,10):
        await asyncio.sleep(0.1)
    Wdisc = False
    Wvoting = True
    while not await WerewolfCountdown(1,15):# TODO: change time to 10
        await asyncio.sleep(0.1)
    Wvoting = False
    killed = random.choice([i for i,x in enumerate(Wvotes) if x == max(Wvotes)])
    await kill(killed,True)


    await client.send_message(channel, "Be quite, the Seer is having a vision!")
    #await client.start_private_message(channelSeer)
    await client.send_message(channelSeer, "Of which person do you want to know if he or she is a Werewolf?")
    SeerActive = True

    while SeerActive:
        await asyncio.sleep(0.1)

    await client.send_message(channel, "Hurry up, I can see the witch just behind this chimney!")
    #await client.start_private_message(channelWitch)
    await client.send_message(channelWitch, "The Person " + str(memberDict[numToId[killed]].name) + " is dying, do you want to give him a second chance or maybe even kill someone else as well?")
    await client.send_message(channelWitch, "Type :-1: to kill someone else too, type :+1: to save the person or type :fist: to do nothing")
    WitchActive = True
    WitchDoingStuff = True
    while WitchDoingStuff:
        await asyncio.sleep(0.1)


async def isDead(playerNumber):
    return deathList[playerNumber]



async def story_day():

    global deaths
    deaths = list(set(deaths))

    if not deaths:
        await client.send_message(channel, "Let's make a party, nobody has died tonight!")
    elif len(deaths) == 1:
        await client.send_message(channel, "Unfortunately one person has died. The one who had to leave us is " + deaths[0])
    else:
        temps = ""
        t = 0
        if len(deaths)!= 2:
            for i in range(len(deaths)-2):
                temps += deaths[i]
                temps += ", "
                t = i
        t+=1
        temps += deaths[t]
        temps += " and "
        temps += deaths[t+1]
        await client.send_message(channel,"Unfortunately some people have died. The ones who had to leave us are " + temps)
def testNumberpair(input):#in: string // max = num Player
    global N
    a = input.split(" ")

    try:
        global b
        b = list(map(int, a))
    except ValueError:
        return False

    if len(b) != 2:
        return False

    if b[0] > 0 and b[0] <= N:
        if b[1] > 0 and b[1] <= N:
            return True
    return False

def testNumberOne(input): #based on 1
    global N

    try:
        a = int(input)
        if(a <= N and a > 0):
            return True
        return False
    except ValueError:
        return False

def isOnline(member):
    if member.status == discord.Status.online:
        return True
    return False
####

client.loop.create_task(timer())
client.run(secrets.token)
