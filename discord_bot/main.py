from __future__ import annotations

import json
import os
import re

import discord
from bot.main import Config
from bot.plugins.youtube_playlist_search import _msg
from discord.ext import commands


client = commands.Bot(command_prefix='!')
token = os.getenv('DISCORD_BOT_TOKEN')


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game('Listening to !explains and !faq'),
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
    # config for heroku
    config = Config(**json.loads(os.getenv('CONFIG')))

    # config for local
    # with open('config.json') as f:
    #   config = Config(**json.load(f))

    line = str(ctx.message.content)
    search_term = re.sub('!explains', '', line)
    get_msg = await _msg(config, 'explains', search_term)

    ESCAPE = {
        ord('\\'): r'\\', ord('_'): r'\_',
        ord('['): r'\[', ord(']'): r'\]',
    }

    def video_title(s: str) -> str:
        return s.strip().translate(ESCAPE)

    await ctx.send(
        f'{ctx.message.author.mention}, '
        f'here you go: {video_title(get_msg)}',
    )


@ client.command(name='faq')
async def faq(ctx):
    # config for heroku
    config = Config(**json.loads(os.getenv('CONFIG')))

    # config for local
    # with open('config.json') as f:
    #   config = Config(**json.loads(f))

    line = str(ctx.message.content)
    search_term = re.sub('!faq', '', line)
    get_msg = await _msg(config, 'faq', search_term)

    ESCAPE = {
        ord('\\'): r'\\', ord('_'): r'\_',
        ord('['): r'\[', ord(']'): r'\]',
    }

    def video_title(s: str) -> str:
        return s.strip().translate(ESCAPE)

    await ctx.send(
        f'{ctx.message.author.mention}, '
        f'here you go: {video_title(get_msg)}',
    )


client.run(token)
