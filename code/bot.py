import logging
import discord
import asyncio
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
###werewolf voting
WinfoSent = False
Wvoting = False
Wdisc = False #discussing
aWerewolfs = 3 #anzahl wölfe
WvotingList = [False for i in range(aWerewolfs)]#AlreadyVoted of W
Wvotes = [0 for i in range(N)]#people to kill
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

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


async def timer():#eventloop with updates all 1/10 of a second
    global CupidInfoSent
    global WinfoSent
    while True:
        if CupidActive and not CupidInfoSent:#Cupid
            await client.send_message(memberDict[numToId[playerCharacters[2][0]]],cupidMessage)
            tempMessage = []
            for i in range(N):
                tempMessage.append(str(N+1) + ": " +memberDict[player[i]].name + "\n")
            s = ''.join(tempMessage)
            await client.send_message(memberDict[numToId[playerCharacters[2][0]]],s)
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
            if message.author.id == numToId[playerCharacters[2][0]]:#if is cupid
                couple = message.content.split(" ")#not checked for wrong input
                CupidActive = False

    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)




client.loop.create_task(timer())
client.run(secrets.username, secrets.password)
