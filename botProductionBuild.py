import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
helperArray = []
randomChannels = []
mainQueue = []
class fileReadWrite():
    file = ""
    def __init__(self,filepath):
        self.file=filepath
    def fileJSONWrite(self,guildID,channelhID):
        with open(self.file,"a") as fileObject:
            fileObject.write(f"^{guildID},{channelhID}")
            fileObject.close()
    def fileGetGuildIDAndChannelID(self,serverGuildID):
        with open(self.file,"r") as fileObject:
            text = fileObject.read()
            fileObject.close()
        tmpStr = ""
        channelStr = False
        channelString = ""
        for i in text:
            tmpStr+=i
            if channelStr:
                channelString += i
            if i == "^":
                channelStr = False
                tmpStr = ""
            if i == ",":
                if tmpStr in serverGuildID or serverGuildID in tmpStr:
                    channelStr = True
                else:
                    channelStr = False
                tmpStr = ""        
        if "^" in channelString:
            channelString = channelString[:-1]                
        return channelString                              
class Server():
    guildID = 0
    helperChannelID = 0    
    def __init__(self,serverID,HelperChannelID):
        self.guildID = self.serverID
        self.helperChannelID = HelperChannelID    
def checkRole(inputRoles,roletocheck):
    helperTrue = False
    for i in inputRoles:
        if i.name == roletocheck:
            helperTrue = True
    return helperTrue
class helper():
    name = ""
    queue = []
    discordUserID = 0
    def __init__(self,newname,discordID):
        self.name = newname
        self.discordUserID = discordID
    def addToQueue(self,data):
        self.queue.append(data)
    def removeMostRecent(self):
        self.queue.pop(0)
bot = commands.Bot(command_prefix='!')
def checkIfloggedIn(ID,ha):
    li = False
    for i in ha:
        if i.discordUserID == ID:
            li = True
    return li
@bot.command(name = "setup", help="Run this on initial setup - requires input of the helpers channel name")
async def setupChannel(ctx, helperchannelname):
    helpersID = 0
    guildID = ctx.message.guild.id    
    for i in ctx.guild.channels:
        if i.name == helperchannelname:
            helpersID = i.id
            files = fileReadWrite("guildInfo.txt")
            files.fileJSONWrite(guildID,helpersID)
            await ctx.send("Your server and helper channel has been added to our list! WOWZERS!")
    if helpersID == 0:
        await ctx.send("Oooooooooooooops that channel doesn't exist :(")
    

    newRole = await ctx.message.guild.create_role(name="loggedIn")
    
@bot.command(name = "getHelperChannel", help = "Run this to get the ID of the Helper Channel", hidden=True)
async def getHelperChannel(ctx,guildID):
    files = fileReadWrite("guildInfo.txt")
    await ctx.send(files.fileGetGuildIDAndChannelID(guildID))
def nonAsyncGetHelperChannel(guildID):
    files = fileReadWrite("guildInfo.txt")
    return files.fileGetGuildIDAndChannelID(guildID)
@bot.command(name="dev", hidden=True)
async def dev(ctx):
    print(helperArray)
@bot.command(name="login", help = "Run this command if you are in the helper channel to set yourself up to take new requests")
async def helperLogin(ctx):
    ID = ctx.author.id
    Name = ctx.message.author.name
    channelSent = str(ctx.message.channel.id)
    guildID = str(ctx.message.guild.id)
    helperChan = nonAsyncGetHelperChannel(str(guildID))    
    if str(channelSent) in str(helperChan) or str(helperChan) in str(channelSent):
        if checkIfloggedIn(ID,helperArray):
            await ctx.send("Oi you are already in our system jog on")
        else:
            newhelper = helper(Name, ID)
            helperArray.append(newhelper)
            #authorRoles = get(ctx.author.roles,"loggedIn")

            loginRoleName = "loggedIn"
            loginRole = get(ctx.guild.roles, name=loginRoleName)
            await ctx.author.add_roles(loginRole)




            await ctx.send("Awwwww look at that you want to help people! Well your wish is granted")


            
    
    else:
        await ctx.send("Ummmmm either wrong place or you ain't no helper! Naughty! ;(")
@bot.command(name="dmmepls", help="Please use this in the format !dmmepls ISSUE TOPIC")
async def dmmepls(ctx, *, Topic):
    guildId = ctx.message.guild.id
    userid = ctx.author.id
    helperChannel = int(nonAsyncGetHelperChannel(str(guildId)))
    helperChannel = bot.get_channel(helperChannel)
    loginRoleName = "loggedIn"
    loginRole = get(ctx.guild.roles, name=loginRoleName)

    await ctx.send("Whoopsy? Looking for some help! Don't worry we have sent it off to our special little helper elves and you'll be put in a channel with one")
    #await helperChannel.send(f'ATTENTION @everyone ! {ctx.author.display_name} requires your assistance with {Topic}!Please type !accept to add them to your queue!')
    await helperChannel.send(f'ATTENTION ! {loginRole.mention} {ctx.author.display_name} requires your assistance with {Topic}!Please type !accept to add them to your queue!')
    mainQueue.append([guildId,userid,ctx.author.display_name,Topic])
@bot.command(name="viewqueue", help="For Helpers - shows the current queue for the server")
async def viewQueue(ctx):
    guildId = ctx.message.guild.id
    userid = ctx.author.id
    helperChannel = int(nonAsyncGetHelperChannel(str(guildId)))
    helperChannel = bot.get_channel(helperChannel)
    loggedIn = checkIfloggedIn(userid, helperArray)    
    if loggedIn:
        guildArray = []
        request = False
        for i in mainQueue:
            if str(i[0]) in str(guildId) or str(guildId) in str(i[0]):
                guildArray.append(i)
                request = True                    
        if not request:
            await ctx.send("well this is awkward...... you don't have any requests for your server")        
        if len(guildArray) > 0:
            for i in guildArray:
                await helperChannel.send(f"Name: {i[2]}  Topic: {i[3]}")        
        if len(mainQueue) == 0:
            await helperChannel.send("There are no requests in the world!")                
    else:
        await ctx.send("Sorry you don't have permission for this")
@bot.command(name="accept", help="For helpers - this command accepts an incoming request and adds it to your queue")    
async def acceptRequest(ctx):
    guildId = ctx.message.guild.id
    userid = ctx.author.id
    helperChannel = int(nonAsyncGetHelperChannel(str(guildId)))
    helperChannel = bot.get_channel(helperChannel)
    loggedIn = checkIfloggedIn(userid, helperArray)
    if loggedIn:
        guildArray = []
        for i in mainQueue:
            if str(i[0]) in str(guildId) or str(guildId) in str(i[0]):
                guildArray.append(i)
                mainQueue.remove(i)            
            else:
                True       
        requestName = guildArray[0][2]
        requestTopic = guildArray[0][3]
        await ctx.send(f"Assigning {requestName} with Topic {requestTopic} to your queue! Please do !startnew to open your latest request OR do !myqueue to see your queue")
        for users in helperArray:
            if str(users.discordUserID) in str(userid) or str(userid) in str(users.discordUserID):
                users.addToQueue(guildArray[0])
    else:
        await ctx.send("Sorry you don't have permission for this")
@bot.command(name="myqueue", help="For helpers - shows the contents of your queue")
async def myQueue(ctx):
    guildId = ctx.message.guild.id
    userid = ctx.author.id
    helperChannel = int(nonAsyncGetHelperChannel(str(guildId)))
    helperChannel = bot.get_channel(helperChannel)
    loggedIn = checkIfloggedIn(userid, helperArray)
    if loggedIn:
        for users in helperArray:
            if str(users.discordUserID) in str(userid) or str(userid) in str(users.discordUserID):
                userqueue = users.queue
        for i in userqueue:
            await ctx.send(f"{i[2]} {i[3]}")
    else:
        await ctx.send("Sorry you don't have permission for this")
def newRandomChannelName():
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    tmpStr = ""
    while True:
        for x in range(0,20):
            tmpStr+= random.choice(alphabet)
        if tmpStr not in randomChannels:
            randomChannels.append(tmpStr)
            break
    return tmpStr    
@bot.command(name="startnew", help="For helpers - this starts the next request in your queue")
async def startNew(ctx):
    guildId = ctx.message.guild.id
    userid = ctx.author.id
    helperChannel = int(nonAsyncGetHelperChannel(str(guildId)))
    helperChannel = bot.get_channel(helperChannel)
    loggedIn = checkIfloggedIn(userid, helperArray)
    target = ""
    for users in helperArray:
        if users.discordUserID == userid:            
            target = users.queue[0][1]
        else:
            target="."
    target = await ctx.guild.fetch_member(target)   
    
    if loggedIn:
        for users in helperArray:
            if users.discordUserID == ctx.author.id:
                users.removeMostRecent()
        newChannelID = newRandomChannelName()
        await ctx.send(f"Message in channel: {newChannelID}")
        category = helperChannel.category
        newRole = await ctx.message.guild.create_role(name=newChannelID)
        channel = await ctx.guild.create_text_channel(newChannelID)
        await target.add_roles(newRole)
        await ctx.author.add_roles(newRole)
        await channel.set_permissions(ctx.guild.default_role, read_messages = False)
        await channel.set_permissions(newRole, read_messages=True)
        await channel.send("Yay you two are together <3 please do !complete when you have finished your little chat :)")
    else:
        await ctx.send("Sorry you don't have permission for this")
@bot.command(name="complete", help="for both helpers and the helped - when you are finishing your 1-to-1 time - one of you must run this command to delete the channel")
async def completeRequest(ctx):
    channelSent = ctx.message.channel
    role_name = ctx.message.channel.name
    if role_name in randomChannels or len(randomChannels) == 0:
        await channelSent.delete()
        role = get(ctx.guild.roles,name=role_name)
        await role.delete()
        await ctx.send("Channel Deleted Daddio")
        randomChannels.remove(role_name)
    else:
        await ctx.send("-_- you cannot use !complete in a non 1-to-1 channel")
@bot.command(name="logout", help="For helpers - use this to log out from accepting requests")
async def logout(ctx):
    user = ctx.message.author.id
    for users in helperArray:
        if user == users.discordUserID:
            helperArray.remove(users)
            loginRoleName = "loggedIn"
            loginRole = get(ctx.guild.roles, name=loginRoleName)
            await ctx.author.remove_roles(loginRole)
            await ctx.send("You are now logged out :) Enjoy the time off")

@bot.command(name="helpers")
async def helperHelp(ctx):
    ID = ctx.author.id
    Name = ctx.message.author.name
    channelSent = str(ctx.message.channel.id)
    guildID = str(ctx.message.guild.id)
    helperChan = nonAsyncGetHelperChannel(str(guildID))    
    if str(channelSent) in str(helperChan) or str(helperChan) in str(channelSent):
        await ctx.send("!accept - This command accepts an incoming request and adds it to your queue\n !complete  for both helpers and the helped - when you are finishing your 1-to-1 call this and it will end your queue request\n !donate - Get a donation Link for the Running of the server\n !login - Run this command if you are in the helper channel to set yourself as available for requests\n !logout  - Use this to log out from accepting requests\n !myqueue - shows the contents of your queue\n !startnew  This starts the next request in your queue\n !viewqueue Shows the current queue for the server")
    else:
        await ctx.send("Ooooooops this can only be called in the helper channel")

@bot.command(name="donate", help ="Get a donation Link for the Running of the server")
async def donate(ctx):
    await ctx.send("https://www.paypal.com/donate?hosted_button_id=WLFD2E3RFGMGS")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Hmmmmmmm we seem to be missing something - Make sure you are giving us a topic or relevant info :)') 
print("Bot is Running")
#Run with the key
bot.run(TOKEN[1:len(TOKEN)-1])
