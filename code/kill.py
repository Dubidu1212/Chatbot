await client.purge_from(channel)




async def makeDead(s):#playerNumber
    global memberDict
    global numToId
    await client.add_roles(memberDict[numToId[s]],discord.utils.get(message.server.roles, name="Dead"))
