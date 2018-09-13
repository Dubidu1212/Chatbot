import logging
import discord
import asyncio
import secrets


logging.basicConfig(level=logging.INFO)
client = discord.Client()

@client.event
async def on_message(message):

    await client.purge_from(message.channel)
    GameServer = message.channel.server
    await client.remove_roles(message.author,discord.utils.get(GameServer.roles, name="sleeping"))
client.run(secrets.token)

async def makeDead(s):#playerNumber
    global memberDict
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="Dead"))
