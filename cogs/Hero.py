import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

headers = {
    'User-Agent':UserAgent().random
}
HERO_URL = 'https://www.dotabuff.com/heroes/'

def Parse_hero_info(hero):
    """Извлечение информации о самых популярных предметов, собираемых героем"""
    r = requests.get(HERO_URL+hero,headers=headers)
    soup = BS(r.content, 'html.parser')
    hero_page = soup.findAll('section')

    #Если герой не найден пишет об ошибке
    if len(hero_page) == 0:
        return 0
    
    # Нахождение блока кода с популярными предметами
    for section in hero_page:
        if "Most Used Items" in section.text:
                hero_items = section
                break

    items_all_info = []

    for td in hero_items.find_all('td'):

        items_all_info.append(td.text)
    
    items = "\n".join(items_all_info[1::5])
    matches = "\n".join(items_all_info[2::5])
    winrates = "\n".join(items_all_info[4::5])

    items_info = {"Items":items, "Matches":matches, "Winrates":winrates}
    return items_info

class Hero(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def hero(self,ctx,*, message: str):
        hero = message.replace(" ","-").lower()
        items_info = Parse_hero_info(hero)
        if items_info == 0:
            await ctx.send('Такого героя не существует. Убедитесь, что имя героя написано правильно.')
        embed_msg = discord.Embed(title=f"Popular items for {hero.replace('-',' ').capitalize()}", color=discord.Color.blue())
        embed_msg.add_field(name="Items", value=items_info['Items'], inline=True)
        embed_msg.add_field(name="Matches", value=items_info['Matches'], inline=True)
        embed_msg.add_field(name="Winrate", value=items_info['Winrates'], inline=True)
        await ctx.send(embed=embed_msg)
    
async def setup(client):
    await client.add_cog(Hero(client))