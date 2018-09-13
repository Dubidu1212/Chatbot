import logging
import discord
import asyncio
import secrets


logging.basicConfig(level=logging.INFO)
client = discord.Client()

@client.event
async def on_message(message):
    await client.send_message(message.channel,message.author.roles[int(message.content)])
    await client.add_roles(message.author,discord.utils.get(message.server.roles, name="Dead"))

client.run(secrets.token)

async def makeDead(s):#playerNumber
    global memberDict
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="Dead"))
