elif WitchActive:
    if message.author.id == numToId[playerCharacter[3][0]]:
        d = message.content.find(":-1:")#thumbsdown
        if d == -1:
            u = message.content.find(":1:")#thumbsup
            if u == -1:
                n = message.content.find(":fist:")#fist
                if n == -1:
                    await client.send_message(message.channel, "Are you trying to kid me?? You have to answer with :-1:,:+1: or :fist:!")
                else:
                    WitchActive = False
                    await client.send_message(message.cannel, "YOu don't feel pity for this poor dude? You're such a witch!")
            else:
                await client.send_message(message.channel, "Ooh you're healing, that's very kind! Maybe this this dude is your secret love?:smirk:")
                # TODO: remove the person from deathList if is in love remove love too
                WitchActive = False
        else:#thumb is down
            await client.send_message(message.channel,"Feeling like killing someone, are you?:skull:")
            # TODO: doing killing stuff
            WitchActive = False
