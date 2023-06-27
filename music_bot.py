import discord
from discord.ext import commands
import os
import asyncio
import youtube_dl
import time

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True


bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command()
async def play(ctx, url):
    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[ctx.guild.id] = voice_client
    except Exception as err:
        print(err)

    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:  # it's a playlist
            song = data['entries'][0]['url']
        else:  # it's a single video
            song = data['url']

        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

        voice_clients[ctx.guild.id].play(player)

    except Exception as err:
        print(err)

@bot.command()
async def pause(ctx):
    try:
        voice_clients[ctx.guild.id].pause()
    except Exception as err:
        print(err)

@bot.command()
async def resume(ctx):
    try:
        voice_clients[ctx.guild.id].resume()
    except Exception as err:
        print(err)

@bot.command()
async def stop(ctx):
    try:
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
    except Exception as err:
        print(err)

@bot.command()
async def help(ctx):
    commands_list = [
        "!play [url] - Plays a song from the provided YouTube URL",
        "!pause - Pauses the currently playing song",
        "!resume - Resumes the paused song",
        "!stop - Stops the currently playing song and disconnects the bot",
        "!help - Shows the list of available commands"
    ]

    help_message = "\n".join(commands_list)
    await ctx.send(f"```{help_message}```")

bot.run("MTEyMzIyMzE1NzcyNjI0OTAwMA.Gi9_Cj.Es6gmUHbYwqWSCWpAYwE_PEoQuUzeNck-re3X8")
