import logging
import discord
import asyncio
import secrets
import vote

logging.basicConfig(level=logging.INFO)
client = discord.Client()
finishedSetup = True

###voting
voting = True
N = 2 #number players
votes = [0 for i in range(N)]
AlreadyVoted = [False for i in range(N)]
###
###werewolf voting
Wvoting = True


###



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
    for(i in range(len(Werwolfs))):
        if(sender.id != Werwolfs[i]){#prevents returning of the message to the sender
            await client.send_message(memberDict[Werwolfs[i]],sender.name + ": " + message)
        }


@client.event
async def on_message(message):
    if(message.author.id == client.user.id):#used so bot doesnt react to own messages
        return
    isPrivate = False
    if(message.channel.name is None):
        isPrivate = True
    if(not isPrivate):#public messages
        if(voting):
            await client.send_message(message.channel,isPrivate)
            if(( len(message.mentions)==1 ) and (not AlreadyVoted[players[message.author.id]])):#stops players from voting twice
                AlreadyVoted[players[message.author.id]] = True
                votes[players[message.raw_mentions[0]]]+=1
    else:#private messages
        for(i in range(aWerewolfs)):
            if(Wvoting and (message.author.id == Werwolfs[i])):#TODO replace Werwolfs
                WMessageRelay(message.content,message.author,Werwolfs)





    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)



client.run(secrets.username, secrets.password)
