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
WitchKilled=False
WitchHealed=False
###
###hunter
HunterActive = False
HunterShoot = False
HunterInfoSent = False
###

LateDeathList = []
###Help
helpmessage1 = ""
helpmessage2 = ""
with open('../resources/help1.txt', 'r') as myfile:
    helpmessage1 = myfile.read()
with open('../resources/help2.txt', 'r') as myfile:
    helpmessage2 = myfile.read()
###
###Infos
killed = -1
numDays = 1
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

debugTime = 1

async def countdown(t,times,ch):#t = time // times = repetitions of t // channel = channel on whitch countdown is sent
    for i in range(times-1):
        await asyncio.sleep(t/debugTime)
        await client.send_message(ch, str(t*times - i*t) + " seconds left")
    return True

async def WerewolfCountdown(t,times):#t = time // times = repetitions of t // channel = channel on whitch countdown is sent
    for i in range(times-1):
        await asyncio.sleep(t)
        await WMessageRelay( str(t*times - i*t) + " seconds left","Narrator")

    return True

async def WMessageRelay(message,sender):#sends all messages to the werwolfs // sender member which sends the message//message //Werwolfs list of id of werwolfs
    if sender == "Narrator":
        for i in range(len(playerCharacter[0])):
            if not deathList[playerCharacter[0][i]]:
                await client.send_message(memberDict[numToId[playerCharacter[0][i]]],message)
    else:
        for i in range(len(playerCharacter[0])):
            if not deathList[playerCharacter[0][i]]:
                if sender.id != numToId[playerCharacter[0][i]] :#prevents returning of the message to the sender
                    await client.send_message(memberDict[numToId[playerCharacter[0][i]]],sender.name + ": " + message)

def checkDeath():


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
        if aRolls > 7:
            deathList[playerCharacter[7][0]] = True
            deaths.append(memberDict[numToId[playerCharacter[7][0]]].name)


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
    global GameServer
    global votes
    global AlreadyVoted
    global deaths
    global deathList
    global WitchHealed
    global WitchKilled

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

            GameServer = message.channel.server
            await client.purge_from(channel)#removes earlyer messages
            mes = await distributeCharacters()
            await client.send_message(channel, mes)
            print(playerCharacter)
            if mes == "Not enough players":
                return
            await asyncio.sleep(3)
            for a in range(N):
                await makeAlive(a)
            for i in range(N):
                await sleep(i)
            await story_first_night()
            x = 0

            while x < 1:
                await story_night()
                for i in range(N):
                    await wake(i)
                await story_day()
                for i in range(N):
                    await sleep(i)

        ##########
        if(voting):
            print(len(message.mentions))
            print(message.raw_mentions[0])
            print(memberDict[message.raw_mentions[0]].name)
            if len(message.mentions)==1  and not AlreadyVoted[players[message.author.id]]:#stops players from voting twice
                AlreadyVoted[players[message.author.id]] = True
                votes[players[message.raw_mentions[0]]]+=1
    else:#private messages

        if HunterActive:
            if message.author.id == numToId[playerCharacter[4][0]]:
                if not testNumberOne(message.content):
                    return
                await client.send_message(message.channel, "With your last breath you shoot through " + memberDict[numToId[int(message.content) - 1]].name + "'s heart")

                await kill(int(int(message.content) - 1),False)
                HunterActive = False
                return

        if isLateDead(players[message.author.id]):#stop people from talking
            await client.send_message(message.author,"You are dead!")
            CupidActive = False
            PriestActive = False
            MidwifeActive = False
            SeerActive = False
            BicycleActive = False
            WitchActive = False
            WitchDoingStuff = False
            return


        if(message.content.lower()=="!help"):
            await client.send_message(message.author, helpmessage1)
            await client.send_message(message.author, helpmessage2)

        if(Wdisc):
            for i in playerCharacter[0]:

                if(message.author.id == numToId[i]):
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
                print(couple)
                print(numToId)

                if couple[0] == couple[1]:
                    await client.send_message(message.author, "I've been told that " + memberDict[numToId[couple[0] - 1]].name + " is not narcisstic!")
                    await client.send_message(message.author, "Choose two diffrent people!")
                    return

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

                if twins[0] == twins[1]:
                    print("Looks good")
                    await client.send_message(message.author, "Seriously?? Have you ever seen someone who is his own twin??")
                    await client.send_message(message.author, "Choose two diffrent people!")
                    return

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
                if int(message.content) - 1 == playerCharacter[1][0]:
                    await client.send_message(message.channel, "Yeah I don't think you're a werewolf:wink:")
                    await client.send_message(message.channel, "Choose someone else!")
                    return

                await client.send_message(message.channel,memberDict[numToId[int(message.content)-1]].name + " is " + temps + "a werewolf")
                SeerActive = False

        elif BicycleActive:
            if message.author.id == numToId[playerCharacter[7][0]]:
                if not testNumberOne(message.content):
                    return

                if int(message.content) - 1 == playerCharacter[7][0]:
                    await client.send_message(message.channel, "Yourself, really?")
                    await client.send_message(message.channel, "Choose someone else!")
                    return


                if playerCharacter[7][0] in twins:
                    if twins.index(playerCharacter[7][0]) == 0:
                        if twins[1] == int(message.content)-1:
                            await client.send_message(message.channel, "Your twin?? That's illegal!!")
                            await client.send_message(message.channel, "Choose someone else!")
                            return
                        else:
                            BicycleVisit = int(message.content) - 1
                            await client.send_message(message.channel,":smirk:")
                            BicycleActive = False
                            return

                    if twins.index(playerCharacter[7][0]) == 1:
                        if twins[0] == int(message.content)-1:
                            await client.send_message(message.channel, "Your twin?? That's illegal!!")
                            await client.send_message(message.channel, "Choose someone else!")
                            return
                        else:
                            BicycleVisit = int(message.content) - 1
                            await client.send_message(message.channel,":smirk:")
                            BicycleActive = False
                            return

                    await client.send_message(message.channel, "Your twin?? That's illegal!!")
                    await client.send_message(message.channel, "Choose someone else!")
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
                        #last<
                        if  ord(message.content)!=9994:
                            await client.send_message(message.channel, "Are you trying to kid me?? You have to answer with :-1:,:+1: or :fist:!")
                        else:
                            WitchActive = False

                            await client.send_message(message.channel, "You don't feel pity for this poor dude? You're such a witch!")
                            WitchDoingStuff = False
                    else:
                        await client.send_message(message.channel, "Ooh you're healing, that's very kind! Maybe this this dude is your secret love?:smirk:")
                        if WitchHealed:
                            await client.send_message(message.channel,"Oh no! You've run out of elixir")
                            WitchDoingStuff = False
                            return
                        #remove the person from deathList if is in love remove love too
                        WitchActive = False
                        WitchHealed = True
                        #last

                        deathList[killed] = False
                        if killed in couple:
                            deathList[couple[1]] = False
                            deathList[couple[0]] = False
                            deaths = [i for i in deaths if i != memberDict[numToId[couple[1]]].name]
                            deaths = [i for i in deaths if i != memberDict[numToId[couple[0]]].name]
                        deaths = [i for i in deaths if i != memberDict[numToId[killed]].name]
                        WitchDoingStuff = False
                else:#thumb is down
                    if WitchKilled:
                        await client.send_message(message.channel,"WITCH NOT KILLING")# TODO:
                        WitchDoingStuff = False
                        return
                    await client.send_message(message.channel,"Feeling like killing someone, are you?:skull:")
                    WitchKilled = True
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
    global LateDeathList
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
    LateDeathList = [False for i in range(N)]
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

        if aRolls >= 7:
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
    global numDays
    global WitchActive
    global Wvoting
    global Wdisc
    global Wvotes
    global WitchDoingStuff
    global name
    global HunterShoot
    global HunterActive
    global killed
    await client.send_message(channel,"==================================Night " + str(numDays) + "==================================")
    channelSeer = memberDict[numToId[playerCharacter[1][0]]]
    channelWitch = memberDict[numToId[playerCharacter[3][0]]]
    await client.send_message(channel, "It turns night in the small village and all the villagers fall asleep!")
    asyncio.sleep(3)

    if aRolls >= 8:

        channelVillageBicycle = memberDict[numToId[playerCharacter[7][0]]]
        if not deathList[playerCharacter[7][0]]:
            await client.send_message(channel, "The Village Bicycle is looking for a new place to stay this night:smirk:")
            #await client.start_private_message(channelVillageBicycle)
            await client.send_message(channelVillageBicycle, "It's getting boring in this, don't you want to look for another one?:smirk:")
            BicycleActive = True
            while BicycleActive:
                await asyncio.sleep(0.1)

    await client.send_message(channel, "I suppose it would be better if you stay at home, **the werewolves are coming!**")
    await asyncio.sleep(3)
    for werewolf in range(len(playerCharacter[0])):
        print(playerCharacter[0])
        print(deathList)
        print(werewolf)
        if not deathList[playerCharacter[0][werewolf]]:
            await client.send_message(memberDict[numToId[playerCharacter[0][werewolf]]], "It smells of human flesh here, aren't you getting hungry?:yum:")

    Wdisc = True
    for werewolf in range(len(playerCharacter[0])):
        if not deathList[playerCharacter[0][werewolf]]:
            await client.send_message(memberDict[numToId[playerCharacter[0][werewolf]]], "You've got 30 seconds to discuss your prey")
    while not await WerewolfCountdown(5,3):
        await asyncio.sleep(0.1)
    Wdisc = False
    Wvoting = True
    while not await WerewolfCountdown(5,2):# TODO: change time to 10
        await asyncio.sleep(0.1)
    Wvoting = False
    killed = random.choice([i for i,x in enumerate(Wvotes) if x == max(Wvotes)])
    await kill(killed,True)

    if not isLateDead(playerCharacter[1][0]):
        await client.send_message(channel, "Be quite, the Seer is having a vision!")
        #await client.start_private_message(channelSeer)
        await client.send_message(channelSeer, "Of which person do you want to know if he or she is a Werewolf?")
        SeerActive = True

    while SeerActive:
        await asyncio.sleep(0.1)

    if not isLateDead(playerCharacter[3][0]):
        await client.send_message(channel, "Hurry up, I can see the Witch just behind this chimney!")
        #await client.start_private_message(channelWitch)
        # TODO: Make gender neutral
        await client.send_message(channelWitch, "The Person " + str(memberDict[numToId[killed]].name) + " is dying, do you want to give him a second chance or maybe even kill someone else as well?")
        await client.send_message(channelWitch, "Type :-1: to kill someone else too, type :+1: to save the person or type :fist: to do nothing")
        WitchActive = True
        WitchDoingStuff = True
    while WitchDoingStuff:
        await asyncio.sleep(0.1)

    #Hunter

    if(aRolls>4):
        if deathList[playerCharacter[4][0]]:
            if not HunterShoot:
                HunterActive = True
                HunterShoot = True
        while HunterActive:
            await asyncio.sleep(0.1)

def isDead(playerNumber):
    global deathList
    return deathList[playerNumber]

def isLateDead(playerNumber):
    global LateDeathList
    return LateDeathList[playerNumber]

async def story_day():
    global numDays
    global voting
    global votes
    global deaths
    global channel
    global HunterActive
    global HunterInfoSent
    global WvotingList
    global Wvotes
    global votes
    global AlreadyVoted
    global N
    global HunterShoot
    global LateDeathList

    await client.send_message(channel,"==================================Day " + str(numDays) + "==================================")
    numDays += 1
    deaths = list(set(deaths))

    for a in range(N):
        if deathList[a]:
            await makeDead(a)


    if not deaths:
        await client.send_message(channel, "Let's make a party, nobody has died tonight!:tada:")
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




    ###discussing-------------------------------------------------------------------------------------------------------------------discussing

    while not await countdown(30,4,channel):
        await asyncio.sleep(0.1)
    while not await countdown(15,3,channel):
        await asyncio.sleep(0.1)
    while not await countdown(5,2,channel):
        await asyncio.sleep(0.1)
    while not await countdown(1,5,channel):
        await asyncio.sleep(0.1)
    ###voting-------------------------------------------------------------------------------------------------------------------voting
    #story

    await client.send_message(channel,"Vote now!")
    voting = True
    while not await countdown(5,5,channel):

        await asyncio.sleep(0.1)
    while not await countdown(1,5,channel):
        await asyncio.sleep(0.1)
    voting= False
    await client.send_message(channel,"1 second left")
    await asyncio.sleep(1)
    await client.send_message(channel,"Stop voting plese")
    print(votes)
    executed = random.choice([i for i,x in enumerate(votes) if x == max(votes)])#playerNumber
    print(executed)
    await client.send_message(channel,memberDict[numToId[executed]].name + " has been hanged on the village square.")

    await kill(executed,False)
    if(aRolls>4):
        if deathList[playerCharacter[4][0]]:
            if not HunterShoot:
                HunterActive = True
                HunterShoot = True
        while HunterActive:
            await asyncio.sleep(0.1)
    for a in range(N):
        if deathList[a]:
            await makeDead(a)
    #------------------------------------------setStartVar

    LateDeathList = deathList
    """
    aWerewolfs = 0
    for wolf in playerCharacter[0]:
        if not deathList[wolf]:
            aWerewolfs+=1

    WvotingList = [False for i in range(aWerewolfs)]
    """
    Wvotes = [0 for i in range(N)]
    votes = [0 for i in range(N)]
    AlreadyVoted = [False for i in range(N)]
    deaths = []


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


async def makeDead(s):#playerNumber
    global memberDict
    global GameServer
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(GameServer.roles, name="Dead"))
    await asyncio.sleep(0.3)

async def makeAlive(s):
    global memberDict
    global numToId
    global GameServer

    await client.remove_roles(memberDict[numToId[s]],discord.utils.get(GameServer.roles, name="Dead"))
    await asyncio.sleep(0.3)

async def sleep(s):
    global memberDict
    global numToId
    global GameServer

    await client.add_roles(memberDict[numToId[s]],discord.utils.get(GameServer.roles, name="sleeping"))
    await asyncio.sleep(0.3)
async def wake(s):
    global memberDict
    global numToId
    global GameServer

    await client.remove_roles(memberDict[numToId[s]],discord.utils.get(GameServer.roles, name="sleeping"))
    await asyncio.sleep(0.3)
####


client.loop.create_task(timer())
client.run(secrets.token)
