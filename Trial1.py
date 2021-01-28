'''
TRIAL TO PLAY AUDIO IN A VOICE CHANNEL
'''

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

with open('creds.txt') as file:
    TOKEN = file.read()
client = commands.Bot(command_prefix = '//')

players = {}

@client.event
async def on_ready():
    print('Bot is alive')

@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.guild
    voice_client = server.voice_client
    await voice_client.disconnect()

##@client.command(pass_context = True)
##async def play(ctx,url):
##    server = ctx.message.guild
##    voice_client = server.voice_client
##    player = await voice_client.create_ytdl_player(url)
##    players[server.id]


@client.command(brief="Plays a single video, from a youtube URL",pass_context = True)
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return

client.run(TOKEN)
