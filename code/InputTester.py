def testNumberpair(in,max):#in: string // max = num Player
    a = in.split(" ")
    if(len(a) != 2):
        return False
    try:
        b = list(map(int,a))
    except ValueError:
        return False
    if b[0]>0 and b[0]<=max:
        if b[1]>0 and b[1]<=max:
            return True
    return False
def testNumberOne(in):
    try:
        a = int(in)
        if(a <= max and a > 0):
            return True
        return False
    except ValueError:
        return False
def isOnline(member):
    if member.status == discord.Status.online:
        return True
    return False
