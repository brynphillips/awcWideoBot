from __future__ import annotations

import json
import os
import re

import discord
from bot.main import Config
from bot.main import get_printed_input
from discord.ext import commands


client = commands.Bot(command_prefix='!')
token = os.getenv('DISCORD_BOT_TOKEN')


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game('Listening to !explains'),
    )
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong with {str(round(client.latency, 2))}')


@client.command(name='whoami')
async def whoami(ctx):
    await ctx.send(f'You are {ctx.message.author.name}')


@client.command(name='explains')
async def explains(ctx):
    #     stdout = sys.stdout
    #     s = StringIO()
    #     sys.stdout = s
    #
    #     config = Config(**json.loads(os.getenv('CONFIG')))
    #     await chat_message_test(config, ctx.message.content)
    #     sys.stdout = stdout
    #     s.seek(0)
    #     readout = s.read()
    config = Config(**json.loads(os.getenv('CONFIG')))
    line = ctx.message.content

    input_returned = await get_printed_input(config, line, images=False)

    answer = re.sub(r'\[[^)]*\]\<[^)]*\>', '', input_returned)
    await ctx.send(f'{ctx.message.author.mention}, here you go: {answer}')


client.run(token)
