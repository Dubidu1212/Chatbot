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

await client.send_message(channel, "I know some of you are suspecting certain villagers to be a werewolf. Now you have the opportunity the vote for someone whom you want to kill. But first, convince the others of your suspicion!")
await client.send_message(channel, "30 seconds to vote!")