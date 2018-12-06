import importlib
import operator
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands

from utils import parse_input

bot = commands.Bot(command_prefix='?')

AVAILABLE = set(range(1, 26))
session:aiohttp.ClientSession = None


@bot.event
async def on_ready():
    global session
    session = aiohttp.ClientSession(cookies={'session': session_token})
    print(f'We have logged in as {bot.user}')


@bot.command()
async def run(ctx, day: int, part: int = 1):
    if day not in AVAILABLE:
        await ctx.send(f'Day {day} not available.')
        return
    if part not in {1, 2}:
        await ctx.send(f'Part {part} not available.')
        return

    try:
        m = importlib.import_module(str(day), 'adventofcode2018')
    except ModuleNotFoundError:
        await ctx.send(f'No solution available for day {day}')
        return

    try:
        f = getattr(m, f'part_{part}')
    except AttributeError:
        await ctx.send(f'No solution available for day {day} part {part}')
        return

    if ctx.message.attachments:
        bytes = BytesIO()
        await ctx.message.attachments[0].save(bytes)
        input = bytes.readlines()
    else:
        input = parse_input(f'input_{day}.txt')

    result = f(input)

    await ctx.send(f'Result for advent {day} part {part}: **{result}**')


STARS = {0:'☆', 1:'★', 2:'⭐'}


@bot.command(aliases=['lb'])
async def leaderbaord(ctx):
    async with session.get('https://adventofcode.com/2018/leaderboard/private/view/378975.json') as resp:
        results = await resp.json()

    embed = discord.Embed(title='Leaderboard 378975')

    max_stars = max(len(m['completion_day_level']) for m in results['members'].values())

    for user in sorted(results['members'].values(), key=operator.itemgetter('stars', 'local_score'), reverse=True):
        stars = ''.join(STARS[len(user['completion_day_level'].get(str(i), {}))] for i in range(1, max_stars+1))
        embed.add_field(name=user['name'], value=stars)

    await ctx.send(embed=embed)


with open('session.txt') as f:
    session_token = f.read()
with open('token.txt') as f:
    token = f.read()
bot.run(token)
