import logging
import discord
import asyncio
import secrets


logging.basicConfig(level=logging.INFO)
client = discord.Client()

@client.event
async def on_message(message):
    print(len(message.mentions))

client.run(secrets.username, secrets.password)
