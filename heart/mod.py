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
from heart.utils.util import format_dt, format_relative
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




class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="had enough?, Mute still annoy u?, Try timeout")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="Valid Member", time="For example, 1d is for 1 day, s for second, m for minutes, h for hour, d for day", reason="The reason")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, time: str, reason: str = None):
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        tempmute = int(time[:-1]) * time_convert[time[-1]]
        await member.timeout(datetime.timedelta(seconds=tempmute), reason=reason)
        embed = discord.Embed(
            title="Timed out", description=f"Timed out user: {member.mention}\n \n For {time} \n \n Tryna Leave ur still can get timed out haha", color=0xe74c3c)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="untimeout", description="Untimeout user")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="Timed out member")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        embed = discord.Embed(
            title="Untimed out", description=f"Untimed out {member.mention}", color=0x2ecc71)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='kick', description='Kick Dumbass from Your Holy Server')
    @app_commands.describe(member="Member About to kicked", reason="Reason")
    @app_commands.checks.has_permissions(kick_members=True)
    async def _kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.guild.kick(Member, reason=reason)
        await interaction.response.send_message(f"{member} Successfully kicked by {interaction.user.mention}")

    @app_commands.command(name='ban', description='Ban dumbass from your Holy Server')
    @app_commands.describe(user="Member About to banned", reason="Reason")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"Successfully banned {user} by {interaction.user.mention}, reason={reason}")

    @app_commands.command(name='unban', description='Unban people who have repented')
    @app_commands.describe(id="ID of Member About to unban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _unban(self, interaction: discord.Interaction, id: int):
        user = await bot.fetch_user(int(id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Unbanned {str(user)}")

    @app_commands.command(name="idban", description="Ban using ID (For Unfair Leaver")
    @app_commands.describe(id="ID of Member About to banned", reason="Reason")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _idban(self, interaction: discord.Interaction, id: discord.User, reason: str = None):
        await interaction.guild.ban(user, reason=reason)
        await imteraction.response.send_message(f"Banned @{user.name}#{user.discriminator}, Reason = {reason}")

    @app_commands.command(name='purge', description='Purge Old Messages')
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(limit="How much ur gonna delete")
    async def _purge(self, interaction: discord.Interaction, limit: int):
        if limit > 100:
            return await interaction.response.send_message("Too much 😖", ephemeral=True)

        messcount = limit
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=messcount)
        await interaction.followup.send(f"Successfully Purged {limit}")
        await interaction.channel.send(f"Purged {limit} messages", delete_after=3)

    @app_commands.command(name='nick', description='Change Nickname of people')
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.describe(member="Member", nick="New Nickname")
    async def chnick(self, interaction: discord.Interaction, member: discord.Member, nick: str):
        await member.edit(nick=nick)
        await interaction.response.send_message(f'Nickname was changed for {member.mention} ')

async def setup(bot):
        await bot.add_cog(Moderation(bot))
