import asqlite
from mystbin import Client
from StringProgressBar import progressBar
from typing import List
import platform
from bs4 import BeautifulSoup
import logging
import aiofiles
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
from dotenv import load_dotenv
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
load_dotenv()
colorama.init(autoreset=True)




class MusicDropDown(discord.ui.Select):
    def __init__(self, track, vc, message):
        ret = []
        self.vc = vc
        self.message = message
        self.executed = False
        for song in track[:10]:
            ret.append(discord.SelectOption(label=song.title,
                       description=song.author, value=song.uri))

        super().__init__(placeholder='Choose song ...',
                         min_values=1, max_values=1, options=ret)

    async def callback(self, interaction: discord.Interaction):

        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        print(self.values[0])
        search = (await self.vc.node.get_tracks(query=self.values[0], cls=wavelink.SoundCloudTrack))[0]
        if self.vc.queue.is_empty and not self.vc.is_playing():
            await self.vc.play(search)
            embed = discord.Embed(
                title="Now playing", description=f"[{search.title}]({search.uri})\n \n Uploader: {search.author}")
            embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
            await self.message.edit(embed=embed, view=None)
        else:
            await self.vc.queue.put_wait(search)
            await self.message.edit(content=f"Added {search.title} to the queue", view=None)
        self.executed = True
        


class MusicSelectView(discord.ui.View):
    def __init__(self, track, vc, userid, message, timeout):
        super().__init__(timeout=timeout)
        self.message = message
        self.dropdown = MusicDropDown(track, vc, message)
        self.add_item(self.dropdown)
        self.userid = userid
        self.vc = vc

    async def on_timeout(self):
        if self.dropdown.executed:
            return True
        else:
            await self.message.edit(content="Music Timed Out", view=None)


    async def interaction_check(self, interaction: discord.Interaction):
        if self.userid != interaction.user.id:
            await interaction.response.send_message("Hey tf are you doing at someones view", ephemeral=True)
        else:
            return True




# music view
class YTMusicDropDown(discord.ui.Select):
    def __init__(self, track, vc, message):
        ret = []
        self.vc = vc
        self.executed = False
        self.message = message
        for song in track[:10]:
            ret.append(discord.SelectOption(label=song.title,
                       description=song.author, value=song.uri))

        super().__init__(placeholder='Choose song ...',
                         min_values=1, max_values=1, options=ret)

    async def callback(self, interaction: discord.Interaction):

        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        search = (await self.vc.node.get_tracks(query=self.values[0], cls=wavelink.YouTubeTrack))[0]
        if self.vc.queue.is_empty and not self.vc.is_playing():
            await self.vc.play(search)
            embed = discord.Embed(
                title="Now playing", description=f"[{search.title}]({search.uri})\n \n Uploader: {search.author}")
            embed.set_thumbnail(url=search.thumbnail)
            embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
            await self.message.edit(embed=embed, view=None)
        else:
            await self.vc.queue.put_wait(search)
            await self.message.edit(content=f"Added {search.title} to the queue", view=None)

        self.executed = True
        


class YTMusicSelectView(discord.ui.View):
    def __init__(self, track, vc, userid, message, timeout):
        super().__init__(timeout=timeout)
        self.message = message
        self.userid = userid
        self.vc = vc
        self.dropdown = YTMusicDropDown(track, vc, self.message)
        self.add_item(self.dropdown)

    async def on_timeout(self):
        if self.dropdown.executed:
            return True
        else:
            await self.message.edit(content="Music Timed Out", view=None)


    async def interaction_check(self, interaction: discord.Interaction):
        if self.userid != interaction.user.id:
            return await interaction.response.send_message("Hey tf are you doing at someones view", ephemeral=True)
        else:
            return True


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
      print(node.identifier)


    @app_commands.command(name="connect", description="Connect to Your Voice")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connected to a voice channel")
        else:
            channel = interaction.user.voice.channel
            vc: wavelink.Player = channel
            await vc.connect(cls=wavelink.Player(node=[n for n in wavelink.NodePool._nodes.values() if n.is_connected()][0]))
            await interaction.followup.send(f"Connected to voice channel: '{channel}'")

    @app_commands.command(name="play", description="Play Youtube (Powered by WaveLink)")
    @app_commands.describe(search="Search for song")
    async def play(self, interaction: discord.Interaction, search: str):
        if not interaction.guild.voice_client:
          if interaction.user.voice is None:
            return await interaction.response.send_message(f"{interaction.user.mention} Your not connected to a voice, connect it!")
          else:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player(node=[n for n in wavelink.NodePool._nodes.values() if n.is_connected()][0]))
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        # detect if user put url instead of title
        await interaction.response.defer(thinking=True)
        if re.fullmatch("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", search):
            scsong = (await vc.node.get_tracks(query=search, cls=wavelink.YouTubeTrack))[0]
            embed = discord.Embed(
                title="Now playing", description=f"[{scsong.title}]({scsong.uri})\n \n Uploader: {scsong.author}")
            embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
            embed.set_thumbnail(url=scsong.thumbnail)
            print(scsong)
            if vc.queue.is_empty and not vc.is_playing():
             await vc.play(scsong)
             await interaction.followup.send(embed=embed)
            else:
             await vc.queue.put_wait(scsong)
             await interaction.followup.send("Added: " + scsong.title)
        else:
            track = await wavelink.YouTubeTrack.search(query=search, return_first=False)
            if not track:
               return await interaction.followup.send("Song not found")
            else:
               await interaction.followup.send(view=YTMusicSelectView(track, vc, interaction.user.id, (await interaction.original_response()), timeout=30), wait=True)
        setattr(vc, "loop", False)
        vc.chan = interaction.channel

    @app_commands.command(name="playsc", description="Play SoundCloud (Powered by WaveLink)")
    @app_commands.describe(search="Search for song")
    async def playsc(self, interaction: discord.Interaction, search: str):
        if not interaction.guild.voice_client:
          if interaction.user.voice is None:
            return await interaction.response.send_message(f"{interaction.user.mention} Your not connected to a voice, connect it!")
          else:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player(node=[n for n in wavelink.NodePool._nodes.values() if n.is_connected()][0]))
        else:
            vc: wavelink.Player = interaction.guild.voice_client
       # detect if user put url instead of title
        await interaction.response.defer(thinking=True)
        if re.fullmatch("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", search):
            scsong = (await vc.node.get_tracks(query=search, cls=wavelink.SoundCloudTrack))[0]
            embed = discord.Embed(
                title="Now playing", description=f"[{scsong.title}]({scsong.uri})\n \n Uploader: {scsong.author}")
            embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
            if vc.queue.is_empty and not vc.is_playing():
             await vc.play(scsong)
             await interaction.followup.send(embed=embed)
            else:
             await vc.queue.put_wait(scsong)
             await interaction.followup.send("Added: " + scsong.title)
        else:
            track = await wavelink.SoundCloudTrack.search(query=search, return_first=False)
            if not track:
             await interaction.followup.send("Song not found")
            else:
             await interaction.followup.send(view=MusicSelectView(track, vc, interaction.user.id, (await interaction.original_response()), timeout=30), wait=True)
        setattr(vc, "loop", False)
        vc.chan = interaction.channel

    @app_commands.command(name="pause", description="Pause song")
    async def pause(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.response.send_message(f"Music paused by {interaction.user.mention}")

    @ app_commands.command(name="resume", description="Resume playing")
    async def resume(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.response.send_message(f"Music is resumed by  {interaction.user.mention}")

    @ app_commands.command(name="stop", description="Stop Player")
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        await interaction.response.send_message(f"{interaction.user.mention} stopped the music.")

    @ app_commands.command(name="disconnect", description="Disconnect the Bot from VC")
    async def disconnect(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.response.send_message(f"{interaction.user.mention} send me out :(")

    @ app_commands.command(name="loop", description="Loops the song")
    async def loop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            embed = discord.Embed(
                title=" ", description="I will now repeat the current track :repeat_one:")
            return await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title=" ", description="I will no longer repeat the current track")
            return await interaction.response.send_message(embed=embed)

    @ app_commands.command(name="queue", description="Show Queues")
    async def queue(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, im not connected to a voice channel")
        elif not interaction.user.voice:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            return await interaction.response.send_message("Queue is empty!")

        em = discord.Embed(color=0x1A2382, title="Queue")
        copy = vc.queue.copy()
        count = 0
        for song in copy:
            count += 1
            em.add_field(name=f"Position {count}", value=f"`{song.title}`")

        return await interaction.response.send_message(embed=em)

    @ app_commands.command(name="volume", description="Volume")
    @ app_commands.describe(volume="Must be 1 to 300")
    async def volume(self, interaction: discord.Interaction, volume: int):
        await interaction.response.defer()
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if volume > 300:
            await vc.set_volume(volume=300)
            embed = discord.Embed(
                title=" ", description=f"Volume has been set to {vc.volume}")
            return await interaction.response.send_message(embed=embed)

        await vc.set_volume(volume=volume)
        embed = discord.Embed(
            title=" ", description=f"Volume has been set to {vc.volume}")
        return await interaction.followup.send(embed=embed)

    @app_commands.command(name="nowplaying", description="Show what playing")
    async def playing(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.response.send_message("Nothing is playing")

        em = discord.Embed(
            title=f" ", description=f"Playing \n **[{vc.track}]({vc.track.uri})** \n Artist: {vc.track.author}")
        em.set_author(name="Now Playing♪", icon_url=f"{self.bot.user.avatar.url}")
        print(vc.track.thumbnail)
        if vc.track.thumbnail is None:
            em.set_thumbnail(
                url="https://media.discordapp.net/attachments/977216545921073192/1033304783156690984/images2.jpg")
        else:
            em.set_thumbnail(url=vc.track.thumbnail)
        bar = progressBar.splitBar(
            int(vc.track.length), int(vc.position), size=10)
        em.add_field(name="Position", value=f"{bar[0]}")
        em.add_field(name="ㅤ", value="ㅤ")
        em.add_field(name="Position",
                     value=f"`{datetime.timedelta(seconds=vc.position)}`")
        em.add_field(name="Duration",
                     value=f"`{datetime.timedelta(seconds=vc.track.length)}`")
        em.set_footer(icon_url=f"{interaction.user.avatar.url}",
                      text=f"Requested by {interaction.user}")
        return await interaction.response.send_message(embed=em)

    @app_commands.command(name="skip", description="Skip a song")
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = discord.Embed(
            title=" ", description=f"[{vc.track}]({vc.track.uri}) has been skipped", color=discord.Color.from_rgb(0, 255, 0))
        await interaction.response.send_message(embed=embed)
        await vc.stop()

    @app_commands.command(name="qremove", description="Remove amount of queue")
    async def qremove(self, interaction: discord.Interaction, index: int):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = ctx.voice_client

        if index > len(vc.queue) or index < 1:
            return await interaction.response.send_message(f"Index must be between 1 and {len(vc.queue)}")

        removed = vc.queue.pop(index - 1)

        await interaction.response.send_message(f"{interaction.user.mention} removed `{removed.title}` from the queue")

    @app_commands.command(name="qclean", description="Clear queue")
    async def qclear(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, you are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            vc.queue.clear()
        return await interaction.response.send_message(f"{interaction.user.mention} cleared the queue.")


async def node_connect(bot):
    await wavelink.NodePool.create_node(bot=bot, host="157.90.181.156", port=7916, password="youshallnotpass")
    await wavelink.NodePool.create_node(bot=bot, host="node1.kartadharta.xyz", port=443, password="kdlavalink", https=True)

async def setup(bot):
    await bot.loop.create_task(node_connect(bot))
    await bot.add_cog(Music(bot))
