import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

headers = {
    'User-Agent': UserAgent().random
}

def hero_counters_get(hero):
    """Получение информации о контрпиках героя"""
    request = requests.get(f'https://www.dotabuff.com/heroes/{hero}', headers=headers)
    soup = bs(request.content, 'html.parser')
    hero_info = soup.find_all('section')

    counters_info = None
    # Поиск блока с информацией о контрпиках героя
    for section in hero_info:

        if 'Worst Versus' in section.text:
            counters_info = section
            break

    # Если не удалось найти информацию о герое
    if counters_info == None:
        return 0

    counters_data = []

    for td in counters_info.find_all('td'):

        counters_data.append(td.text)

    counters_heroes = '\n'.join(counters_data[1::5])
    winrate_versus_counters = '\n'.join(counters_data[3::5])

    counters_result = {
        'Heroes': counters_heroes,
        'Winrates': winrate_versus_counters
    }
    return counters_result

class Counters(commands.Cog):

    def __init__(self, client):

        self.client = client

    @commands.command()
    async def counters(self, ctx, *, message: str):
        
        hero = message.replace(" ","-").lower()
        counters_info = hero_counters_get(hero)

        if counters_info == 0:
            await ctx.send('Такого героя не существует. Убедитесь, что имя героя написано правильно.')
        
        embed_msg = discord.Embed(title=f"Counters {hero.capitalize()}", color=discord.Color.red())
        embed_msg.add_field(name="Hero", value=counters_info['Heroes'], inline=True)
        embed_msg.add_field(name=f"{hero.replace('-',' ').capitalize()}'s Winrate", value=counters_info['Winrates'], inline=True)
        await ctx.send(embed=embed_msg)

async def setup(client):
    await client.add_cog(Counters(client))