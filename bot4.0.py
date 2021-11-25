import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
import mysql.connector




class SQLQueries:
    #Initialises database connection
    def __init__(self):
        self.host = "localhost"
        self.user = "sbcbotdev"
        self.password = "queueme"
        self.database = "QueueMe"

    def isGuild(self,guildID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT GuildID FROM Guilds WHERE GuildID = "+str(guildID))
        myresult = mycursor.fetchall()
        mostRecent = ""
        if len(myresult) > 0:
            return True
        else:
            return False

    #Inserts a new guild
    def insertGuild(self,newGuild,newChannel):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        command = "INSERT INTO Guilds VALUES("+str(newGuild)+","+str(newChannel)+")"
        mycursor.execute(command)
        mydb.commit()
        mydb.close() 
    #Inserts a new queue request
    def insertQueueRequest(self,HelperID,problemID,ProblemDescription, GuildID,targetID):
        try:
            mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mycursor = mydb.cursor()
            command = "INSERT INTO Queue VALUES("+str(GuildID)+","+str(HelperID)+",'"+problemID+"'"+",'"+ProblemDescription+"',"+str(targetID)+")"
            mycursor.execute(command)
            mydb.commit()
            mydb.close() 
        except Exception as e:
            print(e)
    #Returns the helperChannelID
    def getHelperChannelID(self,guildID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT AssistChannel FROM Guilds WHERE GuildID = "+str(guildID))
        myresult = mycursor.fetchall()
        helperChannelID = 0
        for x in myresult:
            helperChannelID = x[0]
        
        mydb.close()
        return helperChannelID
    #Returns the oldest request in the queue
    def getOldestRequest(self,guildID):

        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT problemID FROM Queue WHERE GuildID = "+str(guildID)+" AND HelperID = 0 LIMIT 1")
        myresult = mycursor.fetchall()
        mostRecent = ""
        for x in myresult:
            mostRecent = x[0]
        return mostRecent
    #Returns the helper's next request
    def getHelperNextRequest(self,guildID,HelperID):

        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT problemID FROM Queue WHERE GuildID = "+str(guildID)+" AND HelperID = "+str(HelperID)+" LIMIT 1")
        myresult = mycursor.fetchall()
        mostRecent = ""
        for x in myresult:
            mostRecent = x[0]
        return mostRecent
    # returns a request with a set ID
    def getRequest(self,problemID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Queue WHERE problemID = '"+str(problemID)+"'")
        myresult = mycursor.fetchall()
        return myresult

    #deletes queue for the guild
    def deleteWholeQueue(self,guildID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        command = "DELETE FROM Queue WHERE GuildID = "+str(guildID)
        mycursor.execute(command)
        mydb.commit()
        mydb.close() 
    #sets helper status
    def updateHelper(self,problemID,HelperID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        command = "UPDATE Queue SET HelperID = "+str(HelperID)+" WHERE problemID = '"+problemID+"'"
        mycursor.execute(command)
        mydb.commit()
        mydb.close() 
    #returns the whole queue for a guild
    def getWholeQueue(self,guildID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Queue WHERE GuildID = "+str(guildID))
        myresult = mycursor.fetchall()
        helperChannelID = 0
        return myresult

    #deletes a requst with a set problem id
    def deleteTakenRequest(self,guildID,problemID):
        try:
            mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mycursor = mydb.cursor()
            command = "DELETE FROM Queue WHERE GuildID = "+str(guildID)+" AND problemID = '"+str(problemID)+"'"
            mycursor.execute(command)
            mydb.commit()
            mydb.close() 
        except Exception as e:
            print(e)

    #checks to see if is a helper for the guild
    def isInHelper(self,guildID,helperID):
        mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Helpers WHERE GuildID = "+str(guildID)+" AND HelperID = "+str(helperID))
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            return True
        else:
            return False
    #creates a new helper
    def createHelper(self,guildID,helperID):
        try:
            mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mycursor = mydb.cursor()
            command = "INSERT INTO Helpers VALUES("+str(guildID)+","+str(helperID)+",FALSE)"
            mycursor.execute(command)
            mydb.commit()
            mydb.close() 
        except Exception as e:
            print(e)
    #LogsIn or Logs out
    def setLogIn(self,guildID,helperID,li):
        try:
            mydb = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            mycursor = mydb.cursor()
            command = "UPDATE Helpers SET LoggedIn = "+str(li)+" WHERE GuildID = "+str(guildID)+" AND HelperID = "+str(helperID)
            mycursor.execute(command)
            mydb.commit()
            mydb.close() 
        except Exception as e:
            print(e)

#Creates new random channels
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


#loads the .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#Initialises bot
bot = commands.Bot(command_prefix='Q ')
#sets the name of the log in role
bot.loginRoleName= "Logged In"
bot.SQL = SQLQueries()
randomChannels = []
bot.usedChannels = []

@bot.command(name = "setup", help="Run this on initial setup - requires input of the helpers channel name")
async def setupChannel(ctx, helperchannelname):
    guildID = ctx.message.guild.id  
    found = False
    
    try:                
        for i in ctx.guild.channels:
            helpersID = i.id
            if i.name == helperchannelname and not bot.SQL.isGuild(guildID):              
                category = await ctx.guild.create_category("Assist-Channels")         
                newRole = await ctx.message.guild.create_role(name=bot.loginRoleName)            
                await category.set_permissions(newRole, read_messages=True, send_messages=True)
                await category.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
                bot.SQL.insertGuild(guildID,helpersID)
                await ctx.send("Your server and helper channel has been added to our list! WOWZERS!")
                found = True
        if not found:
            await ctx.send("Ooooooooops seems that channel doesn't exist or your server already is registered, please make sure you've put the name not the ID")
    except Exception as e:
        await ctx.send(e)

def nonAsyncGetHelperChannel(guildID):
    helpc = bot.SQL.getHelperChannelID(guildID)
    return helpc

@bot.command(name="new", help="Start a new queue request")
async def newQueue(ctx, *,topic):
    try:
        guildID = ctx.message.guild.id  
        helperChannel = nonAsyncGetHelperChannel(guildID)
        helperChannel = bot.get_channel(helperChannel)
        loginRole = get(ctx.guild.roles, name=bot.loginRoleName)
        nrcn = newRandomChannelName()
        bot.usedChannels.append(nrcn)
        bot.SQL.insertQueueRequest(0,nrcn,topic, guildID,ctx.author.id)
        await ctx.send("Whoopsy? Looking for some help! Don't worry we have sent it off to our special little helper elves and you'll be put in a channel with one")
        await helperChannel.send(f'ATTENTION ! {loginRole.mention} {ctx.author.display_name} requires your assistance with {topic}!Please type ** Q accept **to add them to your queue!')

    except Exception as e:
        await ctx.send(e)

@bot.command(name="clear", help="Clears the guilds queue", hidden = True)
async def clearQueue(ctx):
    try:
        guildID = ctx.guild.id
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(guildID):

            bot.SQL.deleteWholeQueue(guildID)
            await ctx.send("Queue Cleared")
        else:
            await ctx.send("Uh Uh - you can't do that")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="accept", help="Adds to a helpers queue", hidden = True)
async def acceptRequest(ctx):
    try:
        guildID = ctx.message.guild.id  
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(guildID):
            oldestRequest = bot.SQL.getOldestRequest(ctx.guild.id)
            bot.SQL.updateHelper(oldestRequest,ctx.message.author.id)
            await ctx.send("Added to your queue")
        else:
            await ctx.send("Uh Uh - you can't do that here")
    except Exception as e:
        await ctx.send(e)

@bot.command(name = "viewqueue", help ="Displays Queue", hidden = True)
async def viewQueue(ctx):
    try:
        guildID = ctx.message.guild.id  
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(guildID):
            queue = bot.SQL.getWholeQueue(guildID)
            if len(queue) == 0:
                await ctx.send("No Requests Here :)")
            for i in queue:
                helper = i[1]
                member = i[4]
                member = await ctx.guild.fetch_member(member)
                if helper != 0:
                    helper = await ctx.guild.fetch_member(helper)  
                    helper = helper.display_name                  
                else:
                    helper = "Unassigned"
                    
                await ctx.send("Assigned to: **" + helper+"**   Name: **"+ member.display_name+"**  Topic: **"+i[3]+"**")
        else:
            await ctx.send("Uh Uh - you can't do that here")
    except Exception as e:
        await ctx.send(e)

@bot.command(name = "start", help="Starts your Oldest Queue Request", hidden = True)
async def startRequest(ctx):
    try:
        GuildID = ctx.message.guild.id
        nextR = bot.SQL.getHelperNextRequest(GuildID,ctx.message.author.id)
        requestInfo = bot.SQL.getRequest(nextR)
        target = await ctx.guild.fetch_member(requestInfo[0][4])
        categoryChannel = get(ctx.guild.categories,name="Assist-Channels")
        newRole = await ctx.message.guild.create_role(name=nextR)
        channel = await ctx.guild.create_text_channel(nextR,overrites=None,category = categoryChannel)
        await channel.set_permissions(ctx.guild.default_role, read_messages = False)
        loginRole = get(ctx.guild.roles, name=bot.loginRoleName)
        await channel.set_permissions(loginRole, read_messages = False)
        await channel.set_permissions(newRole, read_messages=True)
        await target.add_roles(newRole)
        await ctx.author.add_roles(newRole)
        await ctx.send(f"Message in channel: {nextR}")
        await channel.send("Yay you two are together <3 please do **Q complete** when you have finished your little chat :)")
        await channel.send("The topic is: **"+requestInfo[0][3]+"**")
        bot.SQL.deleteTakenRequest(GuildID,nextR)
    except Exception as e:
        await ctx.send(e)

@bot.command(name="complete", help="Completes current queue request channel", hidden = True)
async def complete(ctx):
    try:
        channelSent = ctx.message.channel
        role_name = channelSent.name
        if role_name in randomChannels:
            await channelSent.delete()
            role = get(ctx.guild.roles,name=role_name)
            await role.delete()
            randomChannels.remove(role_name)
        else:
            await ctx.send("-_- you cannot perform this in a public channel")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="login", help="Use this to log in", hidden = True)
async def login(ctx):
    try:
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(ctx.guild.id):
            loginRole = get(ctx.guild.roles, name=bot.loginRoleName)
            if not bot.SQL.isInHelper(ctx.guild.id,ctx.message.author.id):
                bot.SQL.createHelper(ctx.guild.id,ctx.message.author.id)
                bot.SQL.setLogIn(ctx.guild.id,ctx.message.author.id, "TRUE")
                await ctx.author.add_roles(loginRole)
                await ctx.send("Awwwww look at that you want to help people! Well your wish is granted")
            else:
                bot.SQL.setLogIn(ctx.guild.id,ctx.message.author.id, "TRUE")
                await ctx.author.add_roles(loginRole)
                await ctx.send("Awwwww look at that you want to help people! Well your wish is granted")
        else:
            await ctx.send("Ummm you can't do this here Sorry")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="logout", help="Use this to log out", hidden = True)
async def logout(ctx):
    try:
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(ctx.guild.id):
            loginRole = get(ctx.guild.roles, name=bot.loginRoleName)
            if not bot.SQL.isInHelper(ctx.guild.id,ctx.message.author.id):
                await ctx.send("You're not recognised on this server - **login** for the first time to be added")
            else:
                bot.SQL.setLogIn(ctx.guild.id,ctx.message.author.id, "FALSE")
                await ctx.author.remove_roles(loginRole)
                await ctx.send("Ahhh - that time already? Take a well earned cuppa and we will see you soon :)")
        else:
            await ctx.send("Ummm you can't do this here Sorry")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="announce", hidden=True)
async def announce(ctx,*,message):
    try:
        if ctx.message.author.id == 224904741715574784:
            for guild in bot.guilds:
                channelID = bot.SQL.getHelperChannelID(guild.id)
                if(channelID != 0):
                    channel = bot.get_channel(channelID)
                    await channel.send(message)
    except Exception as e:
        await ctx.send(e)

@bot.command(name="getGuilds", hidden=True)
async def getGuilds(ctx):
    if ctx.message.author.id == 224904741715574784:
        for guild in bot.guilds:
            await ctx.send(guild.name)


@bot.command(name="HelperCommands", help="shows the commands for helpers")
async def showHelperCommands(ctx):
    try:
        if ctx.message.channel.id == bot.SQL.getHelperChannelID(ctx.guild.id):
            await ctx.send("""
            ***PREFIX IS Q***
    
            **accept** - adds to your queue 
            **clear** - clears the queue for your server
            **complete** - run this once a request is complete in that channel - it will remove it
            **login** - run this to be able to be pinged by a new request
            **logout** - opt out of pings by a new request
            **start** - starts the queue request that is in your queue for the longest
            **viewqueue** - displays the queue for the server    
            """)
        else:
            await ctx.send("You cannot view this here")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="donate", help ="Get a donation Link for the Running of the bot")
async def donate(ctx):
    await ctx.send("https://www.paypal.com/donate?hosted_button_id=WLFD2E3RFGMGS")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Hmmmmmmm we seem to be missing something - Make sure you are giving us a topic or relevant info :)') 
print("Bot is Running")
#Run with the key
bot.run(TOKEN[1:len(TOKEN)-1])
        