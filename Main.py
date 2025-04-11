import discord, os, asyncio
from discord.ext import commands
import json
from config import TOKEN

def get_server_prefix(client, message):
    """Получение префиксов серверов"""
    with open('prefixes.json') as f:
        prefix = json.load(f)

        return prefix[str(message.guild.id)]

client = commands.Bot(command_prefix=get_server_prefix, help_command=None, intents=discord.Intents.all())

@client.event  
async def on_ready():
    """Действия бота при запуске"""
    print(f'Bot {client.user} is active!')

@client.event
async def on_guild_join(guild):
    """Действия при подключении к серверу"""
    with open('prefixes.json') as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = '/'

    with open('prefixes.json', 'w') as f:
        json.dump(prefix,f,indent=4)

@client.event
async def on_guild_remove(guild):
    """Действия при отключении от сервера"""
    with open('prefixes.json') as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefix,f,indent=4)

@client.command()
async def set_prefix(ctx,*, newprefix: str):
    """Установка нового префикса"""
    with open('prefixes.json') as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefix,f,indent=4)

async def load():
    """Загрузка команд из папки cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f"{filename[:-3]} is loaded!")

async def main():
    async with client:
        await load()
        await client.start(TOKEN)
    
if __name__ == "__main__":
    asyncio.run(main())
