import importlib
from discord.ext import commands
from io import BytesIO

from utils import parse_input

bot = commands.Bot(command_prefix='?')

AVAILABLE = set(range(1, 26))


@bot.event
async def on_ready():
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


with open('token.txt') as f:
    token = f.read()
bot.run(token)
