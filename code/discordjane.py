#!/usr/bin/python3
###############################################################################
#         ______ _                       _     ___                            #
#         |  _  (_)                     | |   |_  |                           #
#         | | | |_ ___  ___ ___  _ __ __| |     | | __ _ _ __   ___           #
#         | | | | / __|/ __/ _ \| '__/ _` |     | |/ _` | '_ \ / _ \          #
#         | |/ /| \__ \ (_| (_) | | | (_| | /\__/ / (_| | | | |  __/          #
#         |___/ |_|___/\___\___/|_|  \__,_| \____/ \__,_|_| |_|\___|          #
###############################################################################
# Title           : discordjane.py                                            #
# Description     : Discord automation bot                                    #
# Authot          : Creeva                                                    #
# Date            :                                                           #
# Version         : 1.0                                                       #
# Notes           : https://github.com/creeva/discordjane'                    #
###############################################################################
# Version History                                                             #
#       Version   : 1.0 - Initial Version                                     #
###############################################################################
# Script Setup                                                                #
###############################################################################
#
import datetime
import discord
import glob
import os
from atproto import Client
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
from mastodon import Mastodon
#
###############################################################################
# Variables                                                                   #
###############################################################################
#
# Pulls secrets from .env
#
load_dotenv()
GUILD_ID = os.getenv('GUILD_ID')
GUILD_ID = discord.Object(id=GUILD_ID)
SERVER_ID = os.getenv('SERVER_ID')
MASTODON_TOKEN = os.getenv('MASTODON_TOKEN')
MASTODON_BASE = os.getenv('MASTODON_BASE')
mastodon = Mastodon(access_token=MASTODON_TOKEN, api_base_url=MASTODON_BASE)
#
# General Variables
#
bot_status = cycle(['Awaiting Input', 'Collecting Information'])
logfile = 'logs/discordjanelog.txt'
globalbuffer1 = ''
globalbuffer2 = ''
systemloginfo = '   --   SYSTEM   --   INFO   --   '
systemlogerror = '   --   SYSTEM   --   ERROR   --   '
logtime = '%Y-%m-%d   --   %H:%M:%S'
daytime = '%Y-%m-%d'
checkdocument = f'data/{globalbuffer1}'
inputdata = f'{globalbuffer2}'
#
###############################################################################
# Classes                                                                     #
###############################################################################
#
# Discord Client Commands
#
class Client(commands.Bot):
# Initialization
    async def on_ready(self): 
        change_status.start()
        timestamp = datetime.datetime.now().strftime(logtime)
        print(f'{timestamp}{systemloginfo}Bot Online as {self.user}')
        with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp}{systemloginfo}Bot Online as {self.user}')
# Force slash commands to sync
        try:
            guild = GUILD_ID
            synced = await self.tree.sync(guild=guild)
            timestamp = datetime.datetime.now().strftime(logtime)
            print(f'{timestamp}{systemloginfo}Synced {len(synced)} commands to guild {guild.id}')
            with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp}{systemloginfo}Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e: 
            timestamp = datetime.datetime.now().strftime(logtime)
            print(f'{timestamp}{systemlogerror}Error syncing commands: {e}')
            with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp}{systemlogerror}Error syncing commands: {e}')
# Messages
    async def on_message(self, message):
        if message.author == self.user: return
        if message.content.startswith('status'): await message.channel.send(f'Jane is listening to {message.author}')
        timestamp = datetime.datetime.now().strftime(logtime)
        print(f'{timestamp}   --   DISCORD   --   MESSAGE   --   {message.author}: {message.content}')
        with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp}   --   DISCORD   --   MESSAGE   --   {message.author}: {message.content}')
#
###############################################################################
# Functions                                                                   #
###############################################################################
#
# Consumed - Processes Data Entries
#
async def consumed():
    global globalbuffer1, globalbuffer2
    timestamp = datetime.datetime.now().strftime(logtime)
    date = datetime.datetime.now().strftime(daytime)
    dailyfile = f'daily/{date}-{globalbuffer1}'
    with open(logfile, mode='a', encoding='utf8') as log: 
        print(f'{timestamp}{systemloginfo}{inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp}{systemloginfo}{inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp}{systemloginfo}{inputdata} added to {dailyfile}')
    with open(dailyfile, mode='a+', encoding='utf8') as infile: 
        infile.write(f'\n{inputdata}\n')
        lines = infile.readlines()
    lines.sort()  
    lines = [line for line in lines if line.strip()] 
    with open(dailyfile, 'w') as infile: infile.writelines(lines) 
    with open(checkdocument, mode='a+', encoding='utf8') as infile: 
        infile.write(f'\n{inputdata}\n')
        lines = infile.readlines()
    lines.sort()  
    lines = [line for line in lines if line.strip()] 
    with open(checkdocument, 'w') as infile: infile.writelines(lines) 
#
# Social - Social Media Posts
#
async def socialpost():
    global globalbuffer1, globalbuffer2
    timestamp = datetime.datetime.now().strftime(logtime)
    date = datetime.datetime.now().strftime(daytime)
    dailyfile = f'daily/{date}-{globalbuffer1}'
    with open(logfile, mode='a', encoding='utf8') as log: 
        print(f'{timestamp}{systemloginfo}{inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp}{systemloginfo}{inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp}{systemloginfo}{inputdata} added to {dailyfile}')
    with open(dailyfile, mode='a+', encoding='utf8') as infile: infile.write(f'\n{timestamp}{systemloginfo}{inputdata}\n')
    with open(checkdocument, mode='a+', encoding='utf8') as infile: infile.write(f'\n{timestamp}{systemloginfo}{inputdata}\n')
#
###############################################################################
# Main Script Start                                                           #
###############################################################################
#
# Directory Checking and Creation
#
if not glob.glob('logs'): os.makedirs('logs')
if not glob.glob('data'): os.makedirs('data')
if not glob.glob('daily'): os.makedirs('daily')
#
###############################################################################
# Online Presence                                                             #
###############################################################################
#
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)
#
###############################################################################
# Tasks                                                                       #
###############################################################################
#
# Status Message Rotation
#
@tasks.loop(seconds=30)
async def change_status(): await client.change_presence(activity=discord.Game(next(bot_status)))
#
###############################################################################
# Slash Commands                                                              #
###############################################################################

# Embed
@client.tree.command(name='janeinfo', description='Jane Information', guild=GUILD_ID)
async def janeinfo(interaction: discord.Interaction):
    timestamp = datetime.datetime.now().strftime(logtime)
    with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp}{systemloginfo}Discord Jane Information Displayed')
    embed = discord.Embed(title='Discord Jane Information', url='https://github.com/creeva/discordjane', description='This is an overview of Discord Jane', color=discord.Color.red())
    embed.set_thumbnail(url='https://github.com/creeva/discordjane/raw/main/images/discordjane.png')
    embed.add_field(name='Field 1 Title', value = 'Creeva Wrote This\n next line', inline=False)
    embed.add_field(name='Slash Commands', value = 'Creeva Wrote This 2/n next line', inline=False)
    embed.set_footer(text='Beware this bot was written by a code monkey typing randomly on the keyboard!')
    embed.set_author(name='Jane', url='https://github.com/creeva/discordjane', icon_url='https://github.com/creeva/discordjane/raw/main/images/discordjane.png')
    await interaction.response.send_message(embed=embed)
#
# Books
#
# Read Book   
@client.tree.command(name='read', description='Records read books to a local file', guild=GUILD_ID)
async def readbook(interaction: discord.Interaction, title: str, author: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'readbook.txt'
    globalbuffer2 = f'(::TITLE::){title} (::AUTHOR::){author}'
    await consumed()
    await interaction.response.send_message(f'{title} by {author} was added to the read book list')
# Reading Books
@client.tree.command(name='reading', description='Records books currently being read to a local file', guild=GUILD_ID)
async def reading(interaction: discord.Interaction, title: str, author: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'readingbook.txt'
    globalbuffer2 = f'(::TITLE::){title} (::AUTHOR::){author}'
    await consumed()
    await interaction.response.send_message(f'{title} by {author} was added to the reading list')
# Want To Read Books
@client.tree.command(name='wantbook', description='Records books to be read to a local file', guild=GUILD_ID)
async def wantboo(interaction: discord.Interaction, title: str, author: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'wantbook.txt'
    globalbuffer2 = f'(::TITLE::){title} (::AUTHOR::){author}'
    await consumed()
    await interaction.response.send_message(f'{title} by {author} was added to the want to read list')
# Owned Books
@client.tree.command(name='ownedbook', description='Records owned books to a local file', guild=GUILD_ID)
async def ownedbook(interaction: discord.Interaction, title: str, author: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'ownedbook.txt'
    globalbuffer2 = f'(::TITLE::){title} (::AUTHOR::){author}'
    await consumed()
    await interaction.response.send_message(f'{title} by {author} was added to the owned book list')
#
# Movies
#
# Watched Movies
@client.tree.command(name='watchedmovie', description='Records watched movies to a local file', guild=GUILD_ID)
async def watchedmovie(interaction: discord.Interaction, movie: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'watchedmovie.txt'
    globalbuffer2 = f'{movie}'
    await consumed()
    await interaction.response.send_message(f'{movie} was added to the watched movie list.')
# Want to Watch
@client.tree.command(name='wantmovie', description='Records movies to watch in the future to a local file', guild=GUILD_ID)
async def wantmovie(interaction: discord.Interaction, movie: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'wantmovie.txt'
    globalbuffer2 = f'{movie}'
    await consumed()
    await interaction.response.send_message(f'{movie} was added to the wanted movie list.')
# Owned
@client.tree.command(name='ownedmovie', description='Records owned movies to a local file', guild=GUILD_ID)
async def ownedmovie(interaction: discord.Interaction, movie: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'ownedmovie.txt'
    globalbuffer2 = f'{movie}'
    await consumed()
    await interaction.response.send_message(f'{movie} was added to the owned movie list.')
#
# Music
#
# Owned
@client.tree.command(name='ownedmusic', description='Records owned music to a local file', guild=GUILD_ID)
async def ownedmusic(interaction: discord.Interaction, music: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'ownedmusic.txt'
    globalbuffer2 = f'{music}'
    await consumed()
    await interaction.response.send_message(f'{music} was added to the owned music list.')
# Want - Use to remind user of a certain track or artist
@client.tree.command(name='wantmusic', description='Makes note of artists or songs to track to a local file', guild=GUILD_ID)
async def wantmusic(interaction: discord.Interaction, music: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'wantmusic.txt'
    globalbuffer2 = f'{music}'
    await consumed()
    await interaction.response.send_message(f'{music} was added to the wanted music list.')
#
# Shows
#
# Want to Watch
@client.tree.command(name='wantshow', description='Records shows to watch to a local file', guild=GUILD_ID)
async def wantshow(interaction: discord.Interaction, show: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'wantshow.txt'
    globalbuffer2 = f'{show}'
    await consumed()
    await interaction.response.send_message(f'{show} was added to the shows to watch list.')
# Watched
@client.tree.command(name='watchedepisode', description='Records tv show episodes to a local file', guild=GUILD_ID)
async def watchedepisode(interaction: discord.Interaction, show: str, episode: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'watchedepisode.txt'
    globalbuffer2 = f'(::SHOW::){show} (::EPISODE::){episode}'
    await consumed()
    await interaction.response.send_message(f'{show} episode {episode} was added to the watched episode list.')
# Finished
@client.tree.command(name='watchedshow', description='Records watched show to a local file', guild=GUILD_ID)
async def watchedshow(interaction: discord.Interaction, show: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'watchedshow.txt'
    globalbuffer2 = f'{show}'
    await consumed()
    await interaction.response.send_message(f'{show} was added to the watched show list.')
# Owned
@client.tree.command(name='ownedshow', description='Records owned shows to a local file', guild=GUILD_ID)
async def ownedshow(interaction: discord.Interaction, show: str, season: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'ownedshow.txt'
    globalbuffer2 = f'(::SHOW::){show} (::EPISODE::){season}'
    await consumed()
    await interaction.response.send_message(f'{show} season {season} was added to the watched movie list.')
#
# Video Games
#
# Playing
@client.tree.command(name='playedgame', description='Records played games to a local file', guild=GUILD_ID)
async def playedgame(interaction: discord.Interaction, game: str, platform: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'playedgames.txt'
    globalbuffer2 = f'(::GAME::){game} (::PLATFORM::){platform}'
    await consumed()
    await interaction.response.send_message(f'{game} for {platform} was added to the played games list.')
# Beaten
@client.tree.command(name='beatengame', description='Records beaten games to a local file', guild=GUILD_ID)
async def beatengame(interaction: discord.Interaction, game: str, platform: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'watchedmovies.txt'
    globalbuffer2 = f'(::GAME::){game} (::PLATFORM::){platform}'
    await consumed()
    await interaction.response.send_message(f'{game} for {platform}was added to the beaten game list.')
# Want To Play
@client.tree.command(name='wantgame', description='Records wanted games to a local file', guild=GUILD_ID)
async def wantgame(interaction: discord.Interaction, game: str, platform: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'wantgame.txt'
    globalbuffer2 = f'(::GAME::){game} (::PLATFORM::){platform}'
    await consumed()
    await interaction.response.send_message(f'{game} for {platform} was added to the want to play list.')
# Owned
@client.tree.command(name='ownedgame', description='Records owned games to a local file', guild=GUILD_ID)
async def ownedgame(interaction: discord.Interaction, game: str, platform: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'ownedgame.txt'
    globalbuffer2 = f'(::GAME::){game} (::PLATFORM::){platform}'
    await consumed()
    await interaction.response.send_message(f'{game} for {platform} was added to the owned game list.')
#
# Social
#
# Bluesky
# @client.tree.command(name='bluesky', description='Posts to Bluesky Configured Account', guild=GUILD_ID)
# async def toot(interaction: discord.Interaction, toot: str):
#     global globalbuffer1, globalbuffer2
#     globalbuffer1 = 'bluesky.txt'
#     globalbuffer2 = f'BLUESKY   --   "{toot}"'
#     mastodon.toot(f'{toot}')
#     await socialpost()
#     await interaction.response.send_message(f'"{toot}" posted to Bluesky')
# Mastadon
@client.tree.command(name='toot', description='Posts to Mastodon Configured Account', guild=GUILD_ID)
async def toot(interaction: discord.Interaction, toot: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'mastodon.txt'
    globalbuffer2 = f'MASTODON:"{toot}"'
    mastodon.toot(f'{toot}')
    await socialpost()
    await interaction.response.send_message(f'"{toot}" posted to Mastodon')
#
###############################################################################
# Client Key                                                                  #
###############################################################################
#
client.run(f'{SERVER_ID}')

