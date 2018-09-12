elif WitchActive:
    if message.author.id == numToId[playerCharacter[3][0]]:
        d = message.content.find(":-1:")#thumbsdown
        if d == -1:
            u = message.content.find(":1:")#thumbsup
            if u == -1:
                n = message.content.find(":fist:")#fist
                if n == -1:
                    await client.send_message(message.channel,"You have to answer with :-1:,:+1: or :fist:")
                else:
                    WitchActive = False
                    return
            else:
                await client.send_message(message.channel,"some healing stuff")
                # TODO: remove the person from deathList if is in love remove love too
                WitchActive = False
        else:#thumb is down
            await client.send_message(message.channel,"Feeling like killing someone are you? :skull: ")
            # TODO: doing killing stuff
            WitchActive = False
