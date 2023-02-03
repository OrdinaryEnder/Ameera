import asqlite
from mystbin import Client
from StringProgressBar import progressBar
from typing import List
import platform
from bs4 import BeautifulSoup
import logging
import traceback
import brainfuck
import qrcode
import gc
import colorama
from colorama import Fore, Back, Style
import urllib
import typing
from discord import app_commands
from discord.app_commands import AppCommandError
from discord import Interaction
from discord import ClientException
import re
import os
import subprocess
import math
import functools
import sys
import io
import inspect
import random
import discord
from discord.ext import commands
from discord.ext import tasks
import json
from wavelink import Node as node
import aiohttp
import asyncio
import time
import datetime
import datetime as dt
import typing as t
from email.base64mime import body_encode
import wavelink
from enum import Enum
from discord.utils import get
from discord import NotFound
import itertools
from async_timeout import timeout
from discord.gateway import DiscordWebSocket, _log
from json import loads
import wavelink
import async_timeout
from roblox import Client as Boblox
from roblox import UserNotFound
import toml

colorama.init(autoreset=True)

# this is will cached


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


# setup hook

with open("badwords.txt") as f:
    yudi = f.read()
    badwords = yudi.split()


class MyBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        print(Fore.BLUE + "Registering Commands (Wont take long time)....")
        print(Fore.YELLOW + "Adding cogs")
        for f in os.listdir("./heart"):
            if f.endswith(".py"):
                await bot.load_extension(f"heart.{f[:-3]}")
        await bot.load_extension('jishaku')
        print(Fore.GREEN + "Enabling memory optimizer")
        gc.enable()
        print(Back.WHITE + Fore.RED + "Support" + Fore.YELLOW + " us" + Fore.BLUE +
              " at" + Fore.GREEN + " https://github.com/OrdinaryEnder/Olivia")


intents = discord.Intents().all()
bot = MyBot(command_prefix=commands.when_mentioned, intents=intents,
            activity=discord.Game(name="wassup"))

tree = bot.tree
bot.config = toml.load("config.toml")
bot.startTime = time.time()


@tree.error
async def on_app_command_error(
    interaction: Interaction,
    error: AppCommandError
):
    if isinstance(error, app_commands.CommandOnCooldown):
        if interaction.response.is_done():
            await interaction.followup.send(str(error), ephemeral=True)
        else:
            await interaction.response.send_message(str(error), ephemeral=True)

    elif isinstance(error, app_commands.MissingPermissions):
        if interaction.response.is_done():
            await interaction.followup.send(str(error), ephemeral=True)
        else:
            await interaction.response.send_message(str(error), ephemeral=True)
    else:
        if interaction.response.is_done():
            await interaction.followup.send(str(error), ephemeral=True)
        else:
            await interaction.response.send_message(str(error), ephemeral=True)


@bot.before_invoke
async def deprecate(ctx):
    if ctx.interaction is None:
        if ctx.author.id == 796915832617828352:
            return
        else:
            return await ctx.send("Message command are going EOL \n Ender Been decide to make move too, any command like +meme going to not work \n Prediction: End of October 2022 \n \n INFO: <https://pastebin.com/9Ci5fq96>")


@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(Fore.GREEN + f"Node {node.identifier} is ready!")


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    vc = player

    if vc.loop is True:
        return await vc.play(track)
    try:
        next_song = vc.queue.get()
        await vc.play(next_song)
        embed = discord.Embed(
            title=" ", description=f"Started playing  **[{next_song.title}]({next_song.uri})**")
        await vc.chan.send(embed=embed)
    except wavelink.errors.QueueEmpty:
        embed = discord.Embed(
            title=" ", description="There are no more tracks", color=discord.Color.from_rgb(255, 0, 0))
        await vc.chan.send(embed=embed)
        await vc.disconnect()


@bot.event
async def on_ready():
    print(Back.RED + Fore.BLACK + "Logged As")
    print(Back.WHITE + Fore.BLACK +
          f"@{bot.user.name}#{bot.user.discriminator}")


@bot.event
async def on_member_join(member):
    embed = discord.Embed(title=f"Welcome to {member.guild.name}, {member.name}!",
                          description="By Joining, Your agree to the rules given in server")
    embed.timestamp = datetime.datetime.now()
    await member.send(embed=embed)
    await member.add_roles(member.guild.get_role(os.getenv("MEMBER_ROLE")))


@bot.listen()
async def on_message(message):
    if message.author.bot:
        return

#    if any(badword in message.content.lower().split() for badword in badwords):
#        authorava = await message.author.avatar.read()
#        await message.delete()
#        lmao = await message.channel.create_webhook(name=message.author.name, avatar=authorava)
#        await lmao.send("#" * len(message.content))
#        await lmao.delete()


@bot.event
async def on_guild_join(guild):
        channel = random.choice(guild.channels)
        await channel.send(f"Thanks for adding {bot.user.name}, The Multipurpose bot and Family Friendly")

"""
ZairullahDeveloper once said: Being a developer isnt that easy, start from making mistakes
"""

# Umbras Sync Command


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


class MyHelpCommand(commands.MinimalHelpCommand):

    async def send_pages(self):
        destination = self.get_destination()
        commands = await tree.fetch_commands()
        for command in commands:
            embed = discord.Embed(
                title="Alexandra ", url="https://discord.com/api/oauth2/authorize?client_id=972459217548099584&permissions=0&scope=bot%20applications.commands", description="")
            embed.set_author(name="ZairullahDeveloper", url="https://github.com/zairullahdev",
                             icon_url="https://i.ibb.co/gD6mLh7/Png.png")
            embed.set_thumbnail(
                url="https://i.ibb.co/fp247vT/Untitled1-20220728065509.png")
            embed.add_field(
                name='By OrdinaryEnder Feat ZairullahDeveloper', value='GPL-2.0 License')
            embed.set_footer(
                text="Any suggestions contact ZairullahDeveloper in GitHub (zairullahdev)")
        for page in self.paginator.pages:
            embed.description += page
        await destination.send(embed=embed)


# slash support of help
bot.help_command = MyHelpCommand()

token = os.getenv("TOKEN") or bot.config['main']['token']

bot.run(token)
