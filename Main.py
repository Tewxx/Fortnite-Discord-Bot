import nextcord
from nextcord.ext import commands
import asyncio
import fortnite_api
import random
bot = commands.Bot()

# Put your FN api key in lines 12, 25, 38 & 48
# Put your discord token in line 122

async def UserKills(user: str):
    async with fortnite_api.Client(api_key='Your API Key Here') as client:

        Killstats = await client.fetch_br_stats(name=user)
        Kill_stat_data = Killstats.stats
        Kill_all_stats = Kill_stat_data.all
        Kill_overall_stats = Kill_all_stats.overall

        kills = Kill_overall_stats.kills
        print(kills)
        return int(kills)
        return 0  

async def UserWins(user: str):
    async with fortnite_api.Client(api_key='Your API Key Here') as client:

        Winstats = await client.fetch_br_stats(name=user)
        Win_stat_data = Winstats.stats
        Win_all_stats = Win_stat_data.all
        Win_overall_stats = Win_all_stats.overall

        wins = Win_overall_stats.wins
        print(wins)
        return int(wins)
        return 0 

async def CreatorCode(user: str):
    async with fortnite_api.Client(api_key='Your API Key Here') as client:

        CreatorStats = await client.fetch_creator_code(name=user)
        CreatorCode_stat_data = CreatorStats.account

        print(CreatorCode_stat_data)
        return str(CreatorCode_stat_data)
        return 0 

async def MapUpdate():
    async with fortnite_api.Client(api_key='Your API Key Here') as client:

        Map = await client.fetch_map()
        CurrentMap = Map.images.pois.url


        return (CurrentMap)
        return 0 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(description="Testing Command")
async def ping(interaction: nextcord.Interaction):
    embed = nextcord.Embed(colour=nextcord.Colour.dark_purple(), title="Pong", description=" ")
    await interaction.send(embed=embed)

@bot.slash_command(description="Compare 2 users fortnite stats")
async def compare(interaction: nextcord.Interaction, user1: str, user2: str):

    kills_user1 = await UserKills(user1)
    kills_user2 = await UserKills(user2)
    
    wins_user1 = await UserWins(user1)
    wins_user2 = await UserWins(user2)
	
    if wins_user1 > wins_user2:
        Wins_better_player = user1
        BetterWinsAmount = wins_user1-wins_user2
    elif wins_user1 < wins_user2:
        Wins_better_player = user2
        BetterWinsAmount = wins_user2-wins_user1
    else:
        Wins_better_player = "Both players have equal wins"
        BetterWinsAmount = "Both players have equal wins"
        
    if kills_user1 > kills_user2:
        better_player = user1
        BetterAtKillingPercentBy = kills_user1/kills_user2
        BetterAtKillingPercentBy = round(BetterAtKillingPercentBy, 2)
    elif kills_user1 < kills_user2:
        better_player = user2
        BetterAtKillingPercentBy = kills_user2/kills_user1
        BetterAtKillingPercentBy = round(BetterAtKillingPercentBy, 2)
    else:
        better_player = "Both players have equal kills"
        BetterAtKillingPercentBy = "Both players have equal kills"
    
    comparison_message = f"Comparing ***{user1}*** and ***{user2}***\n\n***Kills:***\n***{user1}***'s Kills: ***{kills_user1}*** \n***{user2}***'s Kills: ***{kills_user2}*** \n***{better_player}*** has more kills by ***{BetterAtKillingPercentBy}x***.\n\n***Wins:***\n***{user1}***' Wins: ***{wins_user1}*** \n***{user2}***'s Wins: ***{wins_user2}*** \n***{Wins_better_player}*** has ***{BetterWinsAmount}*** more wins."
    
    embed = nextcord.Embed(colour=nextcord.Colour.dark_purple(), title="Who's The King Of Fortnite? 👑", description=comparison_message)
    await interaction.send(embed=embed)

@bot.slash_command(description="See the current fortnite map")
async def map(interaction: nextcord.Interaction):
    AwaitedMapUpdate = await (MapUpdate())
    embed = nextcord.Embed(colour=nextcord.Colour.dark_purple())
    embed.set_image(url=AwaitedMapUpdate)
    await interaction.send(embed=embed)

@bot.slash_command(description="See the current fortnite news")
async def news(interaction: nextcord.Interaction):
    embed = nextcord.Embed(colour=nextcord.Colour.dark_purple())
    embed.set_image(url="https://cdn.fortnite-api.com/news/v2/b7679a9d23c6b3950c36a5978a7629a910df5cbb.gif")
    await interaction.send(embed=embed)

@bot.slash_command(description="Get the name of who owns a creator code")
async def codeowner(interaction: nextcord.Interaction, code: str):
    CreatorCodeOwner = await CreatorCode(code)
    creatorcode_message = f"***{CreatorCodeOwner}*** owns the creator code ***{code}***"
    embed = nextcord.Embed(colour=nextcord.Colour.dark_purple(), description=creatorcode_message,)
    await interaction.send(embed=embed)

bot.run('Your token here')
