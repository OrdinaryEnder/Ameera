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
import io
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
from mod.botmod import bypass
from mod.botmod import format_dt, format_relative
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


class refreshbutton(discord.ui.View):
    def __init__(self, userid, timeout):
        super().__init__(timeout=timeout)
        self.value = None
        self.userid = userid

    async def on_timeout(self):
        for butt in self.children:
            butt.disabled = True

        await self.message.edit(view=self)
    # part of slash move, this is cool.

    async def interaction_check(self, interaction: discord.Interaction):
        if self.userid != interaction.user.id:
            return await interaction.response.send_message("Hey tf are you doing at someones view", ephemeral=True)
        else:
            return True

    @discord.ui.button(label="🔄", style=discord.ButtonStyle.grey)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        pages = ["memes",
                 "dankmemes",
                 "PrequelMemes",
                 "terriblefacebookmemes",
                 "wholesomememes",
                 "historymemes",
                 "raimimemes",
                 "linuxmemes"]
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{random.choice(pages)}/new.json?sort=hot') as r:
                res = await r.json()
                embed = discord.Embed(title="Daily Memes", description=" ")
                embed.set_image(url=res['data']['children']
                                [random.randint(0, 25)]['data']['url'])
                await interaction.response.edit_message(embed=embed)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @tasks.loop(seconds=5)
    async def cachelist(self):
        async with aiohttp.ClientSession() as sus:
            async with sus.get("{self.base_url/general/endpoints}") as resp:
                rawdat = await resp.json
                self.imagetypes = [l[10:] for l in rawdat if "/v2/image" in l]

        print("Cached")


    @app_commands.command(name='lvbypass', description='Bypass Linkvertise (powered by bypass.vip)')
    @app_commands.describe(url="URL About to Bypass (Example: https://linkvertise.com/38666/ArceusXRoblox")
    async def _lvbypass(self, interaction: discord.Interaction, url: str):
        link = await bypass(url)
        loadlink = json.dumps(link)
        finalink = json.loads(loadlink)
        print(finalink)
        datalink = finalink.get("destination")
        embed = discord.Embed(
            title="Result", description="Dont let your data get sold by Them!")
        embed.add_field(name="ㅤ", value=datalink)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='8ball', description='Let the 8 Ball Predict!\n')
    @app_commands.describe(question="The question")
    async def _8ball(self, interaction: discord.Interaction, question: str):
        responses = ['As I see it, yes.',
                     'Yes.',
                     'Positive',
                     'From my point of view, yes',
                     'Convinced.',
                     'Most Likley.',
                     'Chances High',
                     'No.',
                     'Negative.',
                     'Not Convinced.',
                     'Perhaps.',
                     'Not Sure',
                     'Maybe',
                     'I cannot predict now.',
                     'Im to lazy to predict.',
                     'I am tired. *proceeds with sleeping*',
                     'Dont ask stupid question like that']
        response = random.choice(responses)
        embed = discord.Embed(title="The Magic 8 Ball has Spoken!")
        embed.add_field(name='Question: ', value=f'{question}', inline=True)
        embed.add_field(name='Answer: ', value=f'{response}', inline=False)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="headortails", description="Head or tails? 🤔")
    async def headtails(self, interaction: discord.Interaction):
            await interaction.response.send_message(f"Its {random.choice(['Head', 'Tails'])}")



    @app_commands.command(name="meme", description="Reddit Memes")
    async def meme(self, interaction: discord.Interaction):
        pages = ["memes",
                 "dankmemes",
                 "PrequelMemes",
                 "terriblefacebookmemes",
                 "wholesomememes",
                 "historymemes",
                 "raimimemes",
                 "linuxmemes"]
        await interaction.response.defer(thinking=True)
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://www.reddit.com/r/{random.choice(pages)}/new.json?sort=hot') as r:
                    res = await r.json()
                    embed = discord.Embed(title="Daily Memes", description=" ")
                    embed.set_image(
                        url=res['data']['children'][random.randint(0, 25)]['data']['url'])

                    view = refreshbutton(interaction.user.id, timeout=30.0)
                    await interaction.followup.send(embed=embed, view=view)
                    view.message = await interaction.original_response()
        except Exception:
            await interaction.followup.send("theres problem", ephemeral=True)

    @app_commands.command(name="linusquotes", description="Get Better Motivation from Linus Torvalds!")
    async def quotes(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://linusquote.com/quote') as r:

                load = await r.json()
                jsonload = json.dumps(load)
                final = json.loads(jsonload)
                print(final['body'])
                embed = discord.Embed(
                    title="Linus Torvalds Once Said:", description="ㅤ")
                embed.add_field(name="ㅤ", value=f"{final['body']}")
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="qrgen", description="Generates QR using Data (Can be URL or Anything")
    @app_commands.describe(data="URL Or String")
    async def qrgen(self, interaction: discord.Interaction, data: str):
        await interaction.response.defer(ephemeral=True)
        img = qrcode.make(data)
        img.save("temp.png")
        embed = discord.Embed(
            title="Successfully Generated", description="Result")
        file = discord.File("temp.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await interaction.followup.send(embed=embed, file=file)
        os.remove("temp.png")

    @app_commands.command(name="generate", description="Generate Image (Powered by JeyyAPI)")
    @app_commands.describe(typeimage="Type Of The Image", image="Can be Member, or URL Image")
    @app_commands.guild_only()
    async def jeyyimage(self, interaction: discord.Interaction, typeimage: str, image: discord.Member = None):
        if typeimage in self.imagetypes:
            async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.bot.config['main']['JEYYAPI_KEY']}"}) as sus:
             async with sus.get(f"{self.base_url + 'image' + typeimage}", params={'image_url': image.display_avatar.url if image else interaction.author.display_avatar.url}) as resp:
                theimg = io.BytesIO(await resp.read())
                myfile = discord.File(theimg, filename="output.png")
                ourembed = discord.Embed(title="Result", description="API Made by Jeyy#6639")
                outembed.set_image(url="attachment://output.png")
                return await interaction.followup.send(embed=ourembed)
        else:
            return await interaction.followup.send(f"{typeimage} is not found")

    @jeyyimage.autocomplete("typeimage")
    async def autocomplete_jeyyapi(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=l, value=l) for l in self.imagetypes if any(pred in current for pred in l)]

     

async def setup(bot):
    await bot.add_cog(Fun(bot))
