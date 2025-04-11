import discord
from discord.ext import tasks,commands
from itertools import cycle

client_status = cycle(['Dota 2'])

class Status(commands.Cog):
    def __init__(self,client):
        
        self.client = client
        self.client_status = client_status

    @commands.Cog.listener()
    async def on_ready(self):

        self.change_status.start()

    @tasks.loop(seconds=5)
    async def change_status(self):
        """Цикличная смена статуса бота"""
        await self.client.change_presence(activity = discord.Game(next(self.client_status)))
    
async def setup(client):
    await client.add_cog(Status(client))