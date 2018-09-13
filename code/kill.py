await client.purge_from(channel)#removes earlyer messages

async def makeDead(s):#playerNumber
    global memberDict
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="Dead"))

async def makeAlive(s):
    global memberDict
    global numToId
    await client.remove_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="Dead"))

async def sleep(s):
    global memberDict
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="sleeping"))
async def wake(s):
    global memberDict
    global numToId
    await client.remove_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="sleeping"))
