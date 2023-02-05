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
from mod.botmod import bypass
from mod.botmod import openairequest
from mod.botmod import format_dt, format_relative
import aiohttp
import asyncio
import time
import datetime
import datetime as dt
import typing as t
from discord.utils import get
from discord import NotFound
import itertools
from async_timeout import timeout
from discord.gateway import DiscordWebSocket, _log
from json import loads
import async_timeout
from roblox import Client as Boblox
from roblox import UserNotFound
from duckpy import AsyncClient as DuckClient

webpaste = Client()
robloxclient = Boblox()
duckyclient = DuckClient()
class Suggestion(discord.ui.Modal, title="Suggestion/Bug Report"):
      suggestion = discord.ui.TextInput(label="Suggestion", placeholder="Type your suggestion/bug report here")
      
      async def on_submit(self, interaction: discord.Interaction):
       async with asqlite.connect('data.db') as conn:
        async with conn.cursor() as cursor:
         await cursor.execute("INSERT INTO suggestion (user, suggestion) VALUES (?, ?)", (f"{interaction.user.name}#{interaction.user.discriminator}", self.suggestion.value))
         await conn.commit()
         return await interaction.response.send_message(f'Thanks for your feedback, {interaction.user.mention}!')

      async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong: \n {error}', ephemeral=True)


class CalculatorView(discord.ui.View):
    def __init__(self, userid):
        super().__init__()
        self.expr = ""
        self.userid = userid

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
            self.expr += "/"
            await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "*"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            self.expr = eval(self.expr)
        except errors.BadArgument: # if you are function only, change this to BadArgument
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "("
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += ")"
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="C", row=4)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        await self.message.edit(content=f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="⌫", row=4)
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = self.expr[:-1]
        await self.message.edit(content=f"```\n{self.expr}\n```")
        
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        return await interaction.response.send_message(str(error), ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction):
        if self.userid != interaction.user.id:
            await interaction.response.send_message("Hey tf are you doing at someones view", ephemeral=True)
        else:
            return True
    async def on_timeout(self):
      for items in self.children:
          items.disabled = True
      await self.message.edit(view=self)



class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.expr_states = {}

    @app_commands.command(name="userinfo", description="Shows info about a user")
    @app_commands.describe(getuser="the user")
    async def info(self, interaction: discord.Interaction,  getuser: typing.Union[discord.Member, discord.User] = None):
        """Shows info about a user."""
        user = interaction.guild.get_member((getuser or interaction.user).id)
        if not user:
            user = await self.bot.fetch_user(getuser.id)
        e = discord.Embed()
        roles = [role.name.replace('@', '@\u200b') for role in getattr(user, 'roles', [])]
        e.set_author(name=str(user))

        def format_date(dt: typing.Optional[datetime.datetime]):
            if dt is None:
                return 'N/A'
            return f'{format_dt(dt, "F")} ({format_relative(dt)})'

        e.add_field(name='ID', value=user.id, inline=False)
        e.add_field(name='Joined', value=format_date(getattr(user, 'joined_at', None)), inline=False)
        e.add_field(name='Created', value=format_date(user.created_at), inline=False)

        voice = getattr(user, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
            e.add_field(name='Voice', value=voice, inline=False)

        if roles:
            e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles', inline=False)

        colour = user.colour
        if colour.value:
            e.colour = colour

        if isinstance(user, discord.User):
            e.set_footer(text='This member is not in this server.')
        else:
            ok = [activity for activity in user.activities if isinstance(activity, discord.Spotify)]
            print(user.activities)
            if ok:
              e.add_field(name="Spotify", value=f"Title: [{ok[0].title}]({ok[0].track_url}) \n Artist: {', '.join(ok[0].artists)} \n Album: {ok[0].album}")


        await interaction.response.send_message(embed=e)

    @app_commands.command(name="finduser", description="Find Roblox Users")
    @app_commands.checks.cooldown(1, 7.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.describe(username="Username")
    async def _boblox(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        em = discord.Embed(title=f"Matching user for {username}")
        try:
         async for users in robloxclient.user_search(username, max_items=10):
            user = await robloxclient.get_user(users.id)
            em.add_field(name=f"Name: **{user.name}**", value=f"Display Name: {user.display_name} \nDescription: {user.description}")
        except UserNotFound:
          await interaction.followup.send("Invalid Username")
        await interaction.followup.send(embed=em)

    @app_commands.command(name="paste", description="Paste something to https://mystb.in")
    @app_commands.checks.cooldown(1, 12.0, key=lambda i: (i.guild_id, i.user.id))
    async def mystpaste(self, interaction: Interaction, text: str):
        await interaction.response.defer()
        textpaste = await webpaste.create_paste(filename="file.txt", content=text)
        await interaction.followup.send(str(textpaste))

    @app_commands.command(name="report", description="Found Bug/Wanna Suggest?, Send a message!")
    async def _report(self, interaction: discord.Interaction):
      await interaction.response.send_modal(Suggestion())

    @app_commands.command(name="invite", description="Invite the bot")
    async def _invite(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=1644971949559&scope=bot", ephemeral=True)

    @app_commands.command(name="list", description="Bunch list of my commands (Need Newer Discord to view this)")
    async def _cmdlist(self, interaction: discord.Interaction):
        cmds = await tree.fetch_commands()
        commands = [
         f"{cmd.mention} - {cmd.description}"
         for cmd in cmds
        ]
        emb = discord.Embed(
          title = "Here are my commands!",
          description = "\n".join(commands)
        )
        await interaction.response.send_message(embed=emb)

    @app_commands.command(name='avatar', description='get someone avatar (avatar copy)')
    @app_commands.describe(avamember="Member")
    async def _avatar(self, interaction: discord.Interaction, avamember: discord.Member = None):
        avamember = avamember or interaction.user
        userAvatarUrl = avamember.avatar.url
        await interaction.response.send_message(userAvatarUrl)

    @commands.command(name='say', description='say smth')
    @commands.is_owner()
    async def _speak(self, ctx, *, text):
        message = ctx.message
        if message.reference:
            await message.delete()
            messagerply = message.reference.message_id
            messagerslt = await ctx.channel.fetch_message(messagerply)
            await messagerslt.reply(f"{text}")
        else:
            await message.delete()
            await ctx.send(f"{text}")
            return

    @app_commands.command(name='brainfuck', description='Yet another BrainFuck Interpreter In Discord')
    @app_commands.describe(code="brainfuck code")
    async def _brainfuck(self, interaction: discord.Interaction, code: str):
        content = re.sub("```brainfuck|```bf|```", "", code)
        bf = brainfuck.evaluate(content)
        if bf:
            embed = discord.Embed(
               title="Result", description="Brainfuck Interpreter")
            embed.add_field(name="Translate:",
                               value=f"{bf}")
        else:
            return await interaction.response.send_message("Invalid Brainfuck")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Pong! <3")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong!\nLatency: {round(self.bot.latency * 1000)}")

    @app_commands.command(name="stats", description="bot stats")
    async def stats(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Bot stats of {self.bot.user}", description="Stats:")
        embed.add_field(
            name="Platform:", value=f"```css \n {platform.system()} {platform.release()} {platform.machine()} \n ```")
        embed.add_field(
            name="Timezone", value=f"```css \n {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo} \n```")
        embed.add_field(
            name="Latency", value=f"```css \n{self.bot.latency * 1000} \n ```")
        embed.add_field(
            name="Uptime", value=f"```css \n {str(datetime.timedelta(seconds=int(round(time.time()-self.bot.startTime))))} \n ```")
        embed.add_field(name="Python Version",
                        value=f"```css \n {sys.version} \n ```")
        embed.add_field(name="Discord.py Version",
                        value=f"```css \n {discord.__version__} \n ```")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="search", description="Search Youtube Videos")
    @app_commands.describe(search="Youtube Video To Search")
    async def yt(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()
        query_string = urllib.parse.urlencode({
            "search_query": search
        })
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string
        )
        search_results = re.findall(
            r"watch\?v=(\S{11})", html_content.read().decode())
        await interaction.followup.send("http://www.youtube.com/watch?v=" + search_results[0])

    @app_commands.command(name="webhookspawn", description="Creates webhook")
    @app_commands.describe(name="Webhook Name")
    @app_commands.checks.has_permissions(manage_webhooks=True)
    async def webhookspawn(self, interaction: discord.Interaction, name: str):
        webhook = await interaction.channel.create_webhook(name=name)
        await interaction.user.send(f"Heres your webhook \n {webhook.url}")
        await interaction.response.send_message(f"Created webhook {name}")

    @app_commands.command(name="uptime", description="bot uptime")
    async def uptime(self, interaction: discord.Interaction):
      await interaction.response.send_message(f"{str(datetime.timedelta(seconds=int(round(time.time()-self.bot.startTime))))}")

    @app_commands.command(name="ducksearch", description="Search With DuckDuckGo!")
    async def goduck(self, interaction: discord.Interaction, searchbar: str):
        await interaction.response.defer()
        result = await duckyclient.search(searchbar)
        embed = discord.Embed(title=f"**Search Matching for {searchbar}**")
        embed.set_author(name="DuckDuckGo", icon_url="https://upload.wikimedia.org/wikipedia/en/9/90/The_DuckDuckGo_Duck.png")
        for results in result[:10]:
            embed.add_field(name="​", value=f"[{results.title}]({results.url}) \n {results.description}")

        await interaction.followup.send(embed=embed)

    @goduck.autocomplete('searchbar')
    async def autocomplete_bar(self, interaction: discord.Interaction, current: str):
        result = await duckyclient.search(current)
        dalist = []
        for results in result[:10]:
           dalist.append(app_commands.Choice(name=results.title, value=results.title))

        return dalist


    @app_commands.command(name="ask", description="Ask Olivia (Powered by OpenAI ChatGPT")
    @app_commands.describe(question="The Question")
    async def chatgpt(self, interaction: discord.Interaction, question: str):
      openaikey = os.getenv("OPENAI_KEY") or self.bot.config['main']['openaikey']
      await interaction.response.defer()
      result = await openairequest(openaikey, question)
      await interaction.followup.send(result)

    @app_commands.command(name="calculator", description="Calculate Something")
    async def basiccalculate(self, interaction: discord.Interaction):
        view = CalculatorView(interaction.user.id)
        await interaction.response.send_message(view=view)
        view.message = await interaction.original_response()
#
async def setup(bot):
    await bot.add_cog(Other(bot))
