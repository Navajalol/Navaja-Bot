import Champions
from re import A
import discord
import random
from discord import channel
from discord.ext import commands
from aiohttp import request
from riotwatcher import LolWatcher
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix = '!')

key = 'RGAPI-ce3ba795-c3b3-49cc-a0fe-9f89377f78d8'
watcher = LolWatcher(key)


def printStats(summonerName):
    summoner = watcher.summoner.by_name('na1', summonerName)
    stats = watcher.league.by_summoner('na1', summoner['id'])
    summonerPUUID = summoner['puuid']
    tier = stats[0]['tier']
    rank = stats[0]['rank']
    lp = stats[0]['leaguePoints']

    wins = int (stats[0]['wins'])
    losses = int (stats[0]['losses'])

    winrate = int (wins/(wins + losses) *100)
    print(tier, rank, lp)
    print(str(winrate) + "%")

    print(summonerName + " is currently ranked in " + str(tier), str(rank) + " with " + str(lp) + " LP and a " + str(winrate) + "% winrate")
    print(summonerPUUID)

printStats("Kittycatmat")


@client.event 

async def on_ready(): 
    print('Bot is ready.')


@client.command(aliases = ['8ball', 'test'])
async def ball8(ctx, *, question):
    responses = ['yes. ', 'No.', 'lol.']
    await ctx.send(f'Answer: {random.choice(responses)}')

@client.command()
async def help3(ctx):
    embedHelp = discord.Embed(
        title = 'Help', 
        description = 'Help command',
        colour = discord.Colour.blue()
    )
    embedHelp.set_footer(text = 'This is a footer.')
    embedHelp.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/236692019693486080/831280838872006675/ninelie.jpg')
    embedHelp.set_author(name = 'Andres', icon_url = 'https://cdn.discordapp.com/attachments/236692019693486080/831280838872006675/ninelie.jpg')
    embedHelp.add_field(name = 'Future commands', value = '!opgg, !rank, !muhammad', inline = False)

    await ctx.send(embed = embedHelp)

@client.command()
async def muhammad(ctx):
    embedMoe = discord.Embed()
    embedMoe.set_image(url = 'https://cdn.discordapp.com/attachments/236692019693486080/831327853815136307/kai_sa.PNG')
    await ctx.send(embed = embedMoe)

#RANKED STATS
@client.command()
async def opgg(ctx, *, args): 

    #STATS
    summoner = watcher.summoner.by_name('na1', args)
    stats = watcher.league.by_summoner('na1', summoner['id'])
    summonerPUUID = summoner['puuid']
    summonerID = summoner['accountId']
    tier = stats[0]['tier']
    rank = stats[0]['rank']
    wins = int (stats[0]['wins'])
    losses = int (stats[0]['losses'])
    lp = stats[0]['leaguePoints']
    winrate = int (wins/(wins + losses) *100)
    
    
    #PRINTING THE STATISTICS
    embedgg = discord.Embed(
        title = f"{args}'s rank", 
        colour = discord.Colour.blue()
    )
    embedgg.add_field(name = 'rank', value = f'{args} is currently ranked in {str(tier)} {str(rank)} with {str(lp)} LP and a {str(winrate)}% winrate', inline = False)

    await ctx.send(embed = embedgg)
    #await ctx.send(f'{args} is currently ranked in {str(tier)} {str(rank)} with {str(lp)} LP and a {str(winrate)}% winrate')
    print(stats)


#LAST GAME COMMAND
@client.command()
async def lastgame(ctx, *, args): 

    
    summoner = watcher.summoner.by_name('na1', args)

    #getting stats from a list of the last 10 games played 
    matchList = watcher.match_v5.matchlist_by_puuid('AMERICAS', summoner['puuid'], 0, 10)

    #getting the ID of the last game 
    Games = matchList[0]
    Games1= matchList[1]
    Games2= matchList[2]
    Games3= matchList[3]
    Games4= matchList[4]


    #getting the match by the id of the game 
    lastgameStats = watcher.match_v5.by_id('AMERICAS', Games)
    lastgameStats1 = watcher.match_v5.by_id('AMERICAS', Games1)
    lastgameStats2 = watcher.match_v5.by_id('AMERICAS', Games2)
    lastgameStats3 = watcher.match_v5.by_id('AMERICAS', Games3)
    lastgameStats4 = watcher.match_v5.by_id('AMERICAS', Games4)


    info = lastgameStats['info']
    info1 = lastgameStats1['info']
    info2 = lastgameStats2['info']
    info3 = lastgameStats3['info']
    info4 = lastgameStats4['info']
    
    Participants = info['participants']
    Participants1 = info1['participants']
    Participants2 = info2['participants']
    Participants3 = info3['participants']
    Participants4 = info4['participants']

    
    
    for y in range(0,5):
        await ctx.send(f'{y+1}: {matchList[y]}')




    await ctx.send('Enter which game you would like to see')    

    #getting input from discord message
    def check(m):
        return  m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["1", "2", "3", "4", "5"]
    msg = await client.wait_for('message', check= check)    
    
    


    if msg.content.lower() == "1":
        for x in range(0,5):
            championid = int(Participants[x]['championId'])
            championid2= int(Participants[x+5]['championId'])
            summonerName = Participants[x]['summonerName']
            summonerName2 = Participants[x+5]['summonerName']
            await ctx.send(f'Player Name: {str(summonerName)}. Champion played: {str(Champions.championDict[championid])}                  Player Name: {str(summonerName2)}. Champion Played {str(Champions.championDict[championid2])}')
            
    elif msg.content.lower() == "2":
        for x in range(0,5):
            championid = int(Participants1[x]['championId'])
            championid2= int(Participants1[x+5]['championId'])
            summonerName = Participants1[x]['summonerName']
            summonerName2 = Participants1[x+5]['summonerName']
            await ctx.send(f'Player Name: {str(summonerName)}. Champion played: {str(Champions.championDict[championid])}                  Player Name: {str(summonerName2)}. Champion Played {str(Champions.championDict[championid2])}')

    elif msg.content.lower() == "3":
        for x in range(0,5):
            championid = int(Participants2[x]['championId'])
            championid2= int(Participants2[x+5]['championId'])
            summonerName = Participants2[x]['summonerName']
            summonerName2 = Participants2[x+5]['summonerName']
            await ctx.send(f'Player Name: {str(summonerName)}. Champion played: {str(Champions.championDict[championid])}                  Player Name: {str(summonerName2)}. Champion Played {str(Champions.championDict[championid2])}')
    elif msg.content.lower() == "4": 
        for x in range(0,5):
            championid = int(Participants3[x]['championId'])
            championid2= int(Participants3[x+5]['championId'])
            summonerName = Participants3[x]['summonerName']
            summonerName2 = Participants3[x+5]['summonerName']
            await ctx.send(f'Player Name: {str(summonerName)}. Champion played: {str(Champions.championDict[championid])}                  Player Name: {str(summonerName2)}. Champion Played {str(Champions.championDict[championid2])}')
    else:     
        for x in range(0,5):
            championid = int(Participants4[x]['championId'])
            championid2= int(Participants4[x+5]['championId'])
            summonerName = Participants4[x]['summonerName']
            summonerName2 = Participants4[x+5]['summonerName']
            await ctx.send(f'Player Name: {str(summonerName)}. Champion played: {str(Champions.championDict[championid])}                  Player Name: {str(summonerName2)}. Champion Played {str(Champions.championDict[championid2])}')

   
    #await ctx.send(f'game ID:\n {Games}'

    
#LIVE COMMAND
@client.command()
async def live(ctx, *, summonerName):
    summonerWatch = watcher.summoner.by_name('na1', summonerName)
    SummonerID = summonerWatch['id']
    liveGame = watcher.spectator.by_summoner('na1', SummonerID)
    Participants = liveGame['participants']
    
    await ctx.send('Blue team:                            Red Team: ')

    for x in range(0,5): 
        championid = int(Participants[x]['championId'])
        championid2= int(Participants[x+5]['championId'])
        summonerId1 = Participants[x]['summonerId']
        summonerId2 = Participants[x+5]['summonerId']
        nameofSummoner = Participants[x]['summonerName']
        nameofSummoner2 = Participants[x+5]['summonerName']
        stats = watcher.league.by_summoner('na1', summonerId1)
        stats2 = watcher.league.by_summoner('na1', summonerId2)
        tier = stats[0]['tier']
        rank = stats[0]['rank']
        tier2 = stats2[0]['tier']
        rank2 = stats2[0]['rank']

        if tier is None:
             await ctx.send(f'Player Name: {str(nameofSummoner)}. Champion:{str(Champions.championDict[championid])} Rank: UNRANKED         Player Name: {str(nameofSummoner2)}. Champion: {str(Champions.championDict[championid2])} Rank: {str(tier2)} {str(rank2)} ')
        if tier2 is None:
             await ctx.send(f'Player Name: {str(nameofSummoner)}. Champion:{str(Champions.championDict[championid])} Rank: {str(tier)} {str(rank)}                 Player Name: {str(nameofSummoner2)}. Champion: {str(Champions.championDict[championid2])} Rank: UNRANKED ')     

        if tier is None and tier2 is None:
             await ctx.send(f'Player Name: {str(nameofSummoner)}. Champion:{str(Champions.championDict[championid])} Rank: UNRANKED                Player Name: {str(nameofSummoner2)}. Champion: {str(Champions.championDict[championid2])} Rank: UNRANKED ')     
        
        
        #if all the players have a rank in ranked/solo
        await ctx.send(f'Player Name: {str(nameofSummoner)}. Champion:{str(Champions.championDict[championid])} Rank: {str(tier)} {str(rank)}         Player Name: {str(nameofSummoner2)}. Champion: {str(Champions.championDict[championid2])} Rank: {str(tier2)} {str(rank2)} ')
    

# LEVEL COMMAND
@client.command()
async def level(ctx, *, summoner): 
    summonerWatch = watcher.summoner.by_name('na1', summoner)
    summonerLevel = summonerWatch['summonerLevel']
    
    await ctx.send( summoner + " is level " + str(summonerLevel))

    

client.run('ODMwMjA4NzExODA0MTkwNzMw.YHDWHQ.Dk4IXZYyskePLSsTVOIuAlx7ztU')