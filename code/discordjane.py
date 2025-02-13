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
# Date            :                                                           #
# Version         : 1.0                                                       #
# Notes           :                                                           #
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
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
from os import name
#
###############################################################################
# Variables                                                                   #
###############################################################################
#
bot_status = cycle(['Awaiting Input', 'Collecting Information'])
current_time = datetime.datetime.now()
month = (current_time.month)
day = (current_time.day)
logfile = 'logs/discordjanelog.txt'
globalbuffer1 = ''
globalbuffer2 = ''
#
# Defines Automation Discord Server
#
GUILD_ID = discord.Object(id=PUTGUILDIDHERE)
SERVER_ID = 'PUTSERVERIDHERE'
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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")
        print(f'{timestamp} -- SYSTEM -- Bot Online as {self.user}')
        with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp} -- SYSTEM -- Bot Online as {self.user}')
# Force slash commands to sync
        try:
            guild = GUILD_ID
            synced = await self.tree.sync(guild=guild)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")
            print(f'{timestamp} -- SYSTEM -- Synced {len(synced)} commands to guild {guild.id}')
            with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp} -- SYSTEM -- Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e: 
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")
            print(f'{timestamp} -- ERROR -- Error syncing commands: {e}')
            with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp} -- ERROR -- Error syncing commands: {e}')
# Messages
    async def on_message(self, message):
        if message.author == self.user: return
        if message.content.startswith('hello'): await message.channel.send(f'Hello {message.author}')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d -- %H:%M:%S")
        print(f'{timestamp} -- MESSAGE -- {message.author}: {message.content}')
        with open(logfile, mode='a', encoding='utf8') as log: log.write(f'\n{timestamp} -- MESSAGE -- {message.author}: {message.content}')
#
###############################################################################
# Functions                                                                   #
###############################################################################
#
async def consumed():
    global globalbuffer1, globalbuffer2
    checkdocument = f'data/{globalbuffer1}'
    inputdata = f'{globalbuffer2}'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d -- %H:%M:%S')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    dailyfile = f'daily/{date}-{globalbuffer1}'
    with open(logfile, mode='a', encoding='utf8') as log: 
        print(f'{timestamp} -- DATAENTRY -- {inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp} -- DATAENTRY -- {inputdata} added to {checkdocument}')
        log.write(f'\n{timestamp} -- DATAENTRY -- {inputdata} added to {dailyfile}')
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
@tasks.loop(seconds=30)
async def change_status(): await client.change_presence(activity=discord.Game(next(bot_status)))
#
###############################################################################
# Slash Commands                                                              #
###############################################################################
#
# Read Book
#    
@client.tree.command(name='readbook', description='Records read books to a local file', guild=GUILD_ID)
async def readbook(interaction: discord.Interaction, inputdata: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'readbook.txt'
    globalbuffer2 = f'{inputdata}'
    await consumed()
    await interaction.response.send_message(f'{inputdata} was added to the read book list')
#
# Watched Movies
# 
@client.tree.command(name='watchedmovie', description='Records watched movies to a local file', guild=GUILD_ID)
async def watchedmovie(interaction: discord.Interaction, inputdata: str):
    global globalbuffer1, globalbuffer2
    globalbuffer1 = 'watchedmovies.txt'
    globalbuffer2 = f'{inputdata}'
    await consumed()
    await interaction.response.send_message(f'{inputdata} was added to the watched movie list.')
#
###############################################################################
# Client Key                                                                  #
###############################################################################
#
client.run(f'{SERVER_ID}')