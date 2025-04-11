from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

headers ={
    "user-agent": UserAgent().random
} 

META_URL = 'https://www.dotabuff.com/heroes?show=heroes&view=meta&mode=all-pick&date=7d&rankTier=immortal'

r = requests.get(META_URL,headers=headers)

def Parse_meta_info():
    """Получение информации о метовых героях"""
    soup = BS(r.content,"html.parser" )
    names_find = soup.findAll('div', class_ = 'tw-flex tw-flex-col tw-gap-0')

    for i in range(10):
        names_find[i] = names_find[i].text

    names_find = '\n'.join(names_find[:10])

    pickrates_and_winrates_find = soup.findAll('div', class_ = 'tw-flex tw-w-full tw-flex-col tw-items-start tw-gap-1')
    for i in range(0,50,5):
        pickrates_and_winrates_find[i] = pickrates_and_winrates_find[i].text
    for i in range(2,52,5):
        pickrates_and_winrates_find[i] = pickrates_and_winrates_find[i].text

    winrates = '\n'.join(pickrates_and_winrates_find[:50:5])
    pickrates = '\n'.join(pickrates_and_winrates_find[2:52:5])

    heroes = {'Hero': names_find ,'Winrate': winrates, 'Pickrate': pickrates}
    return heroes
    
class Meta(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def meta(self, ctx):
        heroes = Parse_meta_info()
        embed_msg = discord.Embed(title="Meta", color=discord.Color.blue())
        embed_msg.add_field(name="Hero", value=heroes['Hero'], inline=True)
        embed_msg.add_field(name="Winrate", value=heroes['Winrate'], inline=True)
        embed_msg.add_field(name="Pickrate", value=heroes['Pickrate'], inline=True)
        await ctx.send(embed=embed_msg)

async def setup(client):
    await client.add_cog(Meta(client))