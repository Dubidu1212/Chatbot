import logging
import discord
import asyncio
import secrets


logging.basicConfig(level=logging.INFO)
client = discord.Client()

@client.event
async def on_message(message):
    await client.send_message(,"Dubidu1212: "+message.content)

client.run()
