import discord
from bot.main import *
from discord.ext import commands
from io import StringIO
import sys
import os
import re

client = commands.Bot(command_prefix = '!')
token = os.getenv('DISCORD_BOT_TOKEN')
config = Config(
    "...",
    "...",
    "...",
    "...",
    os.environ['youtube_api_key'],}
    "youtube_playlists": {
        "explains": {
            "playlist_id": "PLWBKAf81pmOaP9naRiNAqug6EBnkPakvY",
            "github": "https://github.com/anthonywritescode/explains"
        },
        "faq": {
            "playlist_id": "PLWBKAf81pmOZEPeIV2_pIESK5hRMAo1hR"
        },
    "..."
    )




@client.event
async def on_ready():
    await client.change_presence(
        status = discord.Status.idle,
        activity = discord.Game('Listening to .help')
        )
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong with {str(round(client.latency, 2))}')

@client.command(name = 'whoami')
async def whoami(ctx):
    await ctx.send(f'You are {ctx.message.author.name}')

@client.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)

@client.command(name = 'explains')
async def explains(ctx):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json')
    parser.add_argument('--verbose', action='store_true')
    # parser.add_argument('--images', action='store_true')
    # parser.add_argument('--test')
    args = parser.parse_args()

    stdout = sys.stdout
    s = StringIO()
    sys.stdout = s

    quiet = not args.verbose

    with open(args.config) as f:
        config = Config(**json.load(f))
        await chat_message_test(config,ctx.message.content)
        sys.stdout = stdout
        s.seek(0)
        readout = s.read()
        f.close()

    answer = re.sub(r'\[[^)]*\]\<[^)]*\>', '', readout)
    await ctx.send(f'{ctx.message.author.mention}, here you go: {answer}')


client.run(token)

