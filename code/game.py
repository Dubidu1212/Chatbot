import discord
import logging
import secrets
import random

logging.basicConfig(level = logging.INFO)
client = discord.Client()

server = discord.Server
started = False
characters = ["Seer", "Witch", "Cupid", "Hunter", "Midwife", "Priest", "Village bicycle"]
players = {} #dictionary key: player's id, value: player's number
playerCharacter = {} #dictionary key: player's number, value: his character

@client.event
async def on_message(message):
    if message.content.lower() == "start" and not started: #if the message is "started and the game isn't
                                                                  # started yet, start it
        aMembers = server.member_count #number of members
        members = server.members #all members
        occupated = [False for a in range(aMembers - 1)] #store the characters which are already taken

        if aMembers < 5: #there must be at least 5 players
            print("Not enough players")
            return

        aWerewolfs = int(round(aMembers * 0.3, 0)) #number of werewolfs (30%)
        count = 0

        for a in members:
            players[a.id] = count #assign a number to each player
            ran = random.randint(0, aMembers - 1) #pick a random role for this player

            while occupated[ran]: #if this roll is already taken, look for another one
                ran = random.randint(0, aMembers - 1)

            occupated[ran] = True

            if ran >= 6 + aWerewolfs:
                playerCharacter[count] = "Villager"
            elif ran <= aWerewolfs:
                playerCharacter[count] = "Werewolf"
            else:
                playerCharacter[count] = characters[ran]

            count += 1

client.run(secrets.username, secrets.password)
