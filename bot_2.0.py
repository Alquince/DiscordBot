# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from Generador import *
import random
import os
import requests

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def password(ctx, long: int=8):
    await ctx.send("Tu contraseña es: ")
    await ctx.send(gen_pass(long))

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

# ////////////////////////////////////////   

@bot.command()
async def ping(ctx):
    """Responde con la latencia del bot."""
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

# ///////////////////////////////////////

@bot.command()
async def mem(ctx):
    meme = random.choice(os.listdir("memes"))
    with open(f'memes/{meme}', 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# Tipos de memes

@bot.command()
async def mem_categoria(ctx, categoria: str):
    memes = {
        "anime": [
            {"url": "https://i.pinimg.com/736x/5f/ce/c9/5fcec9a35213920b724f2a04676e3204.jpg", "rareza": 0.4},    
            {"url": "https://images7.memedroid.com/images/UPLOADED246/64d4a8a6d3263.jpeg", "rareza": 0.6}   
        ],
        "tecnologia": [
            {"url": "https://www.boredpanda.es/blog/wp-content/uploads/2022/03/20-6228a4eb3d3ec_1u9oohepwsi81__700-622b145752c46__700.jpg", "rareza": 0.3},
            {"url": "https://www.boredpanda.es/blog/wp-content/uploads/2022/03/03-6228a2ac81c49_hwurhp7crzf81-png__700-622b13a1722c6__700.jpg", "rareza": 0.5}
        ]
    }

    if categoria not in memes:
        await ctx.send("Categoría no encontrada. Categorías disponibles: " + ", ".join(memes.keys()))
        return

    lista_memes = memes[categoria]
    pesos = [(1 - meme["rareza"]) for meme in lista_memes]
    meme_seleccionado = random.choices(lista_memes, weights=pesos, k=1)[0]
    meme_url = meme_seleccionado["url"]

    embed = discord.Embed(title=f"Meme de {categoria}")
    embed.set_image(url=meme_url)
    await ctx.send(embed=embed)


bot.run('TOKEN')
