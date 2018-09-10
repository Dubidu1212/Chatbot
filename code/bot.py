import logging
import discord
import asyncio
import secrets
import vote

logging.basicConfig(level=logging.INFO)
client = discord.Client()
finishedSetup = True
voting = True
N = 2#number players
votes = [0 for i in range(N)]
AlreadyVoted = [False for i in range(N)]



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

@client.event
async def on_message(message):
    if(message.author.id == client.user.id):
        return
    if(voting):
        await countdown(1,5,message.channel)
        if(( len(message.mentions)==1 ) and (not AlreadyVoted[players[message.author.id]])):

            AlreadyVoted[players[message.author.id]] = True
            votes[players[message.raw_mentions[0]]]+=1


    #if message.content.startswith():
    #    await client.send_message(message.channel,message.channel.name)



client.run(secrets.username, secrets.password)
