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
colorama.init(autoreset=True)




class MusicDropDown(discord.ui.Select):
    def __init__(self, track, vc, message):
        ret = []
        self.lel = {} # because long ass sc links
        self.vc = vc
        self.message = message
        self.executed = False
        for index, song in enumrate(track[:10]):
            ret.append(discord.SelectOption(label=song.title,
                       description=song.author, value=str(index)))
            self.lel[song.title] = song.uri

        super().__init__(placeholder='Choose song ...',
                         min_values=1, max_values=1, options=ret)

    async def callback(self, interaction: discord.Interaction):

        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        print(self.values[0])
        search = (await wavelink.NodePool.get_connected_node().get_tracks(query=self.lel[self.values[0]], cls=wavelink.SoundCloudTrack))[0]
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
        search = (await wavelink.NodePool.get_connected_node().get_tracks(query=self.values[0], cls=wavelink.YouTubeTrack))[0]
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
        self.leave_check = {}
        self.lock = asyncio.Lock()

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
      print(node.id)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
     vc = payload.player

     if vc.loop is True:
        return await vc.play(track)
     try:
        next_song = vc.queue.get()
        await vc.play(next_song)
        embed = discord.Embed(
            title=" ", description=f"Started playing  **[{next_song.title}]({next_song.uri})**")
        await vc.chan.send(embed=embed)
     except wavelink.QueueEmpty:
        embed = discord.Embed(
            title=" ", description="There are no more tracks", color=discord.Color.from_rgb(255, 0, 0))
        await vc.chan.send(embed=embed)
        await vc.disconnect()


        # bot disconnected itself

    async def cog_unload(self):
        node = wavelink.NodePool.nodes
        for sus in node:
            await node.disconnect()

    filterscmd = app_commands.Group(name="filter",  description="Set Filter")
    @filterscmd.command(name="bassboost", description="Set Bass Boost")
    async def bassbooster(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connexted to a voice channel")
        elif not interaction.guild.voice_client:
            return await interaction.followup.send("No such voice connected")
        else:
            # prob the best eq values for bass boost
            bands = [
    (0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),
    (5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1),
    (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, -0.1)
]
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer(name="Bass Boost", bands=bands)))
            return await interaction.followup.send("Set Filter: Bass Boost")

    @filterscmd.command(name="nightcore", description="Set Nightcore")
    async def nightcore(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connexted to a voice channel")
        elif not interaction.guild.voice_client:
            return await interaction.followup.send("No such voice connected")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.set_filter(wavelink.Filter(timescale=wavelink.Timescale(speed=1.1, pitch=1.2, rate=1.1)))
            return await interaction.followup.send("Set Filter: Nightcore")

    @filterscmd.command(name="clear", description="Clear Filters")
    async def cleareffect(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connexted to a voice channel")
        elif not interaction.guild.voice_client:
            return await interaction.followup.send("No such voice connected")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.set_filter(wavelink.Filter(equalizer=None, timescale=None))
            return await interaction.followup.send("Cleared Filters")

    @filterscmd.command(name="sloweffect", description="Set Slowdown Filter")
    async def sloweffect(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connexted to a voice channel")
        elif not interaction.guild.voice_client:
            return await interaction.followup.send("No such voice connected")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.set_filter(wavelink.Filter(timescale=wavelink.Timescale(speed=0.9, pitch=0.9, rate=0.9)))
            await interaction.followup.send("Set Filter: Slowdown")

    @app_commands.command(name="connect", description="Connect to Your Voice")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not interaction.user.voice:
            return await interaction.followup.send("You are not connected to a voice channel")
        else:
            channel = interaction.user.voice.channel
            vc: wavelink.Player = channel
            await vc.connect(cls=wavelink.Player())
            if interaction.guild in self.leave_check:
                del self.leave_check[interaction.guild]
                self.leave_check[interaction.guild.id] = True
            else:
                self.leave_check[interaction.guild.id] = True
            await interaction.followup.send(f"Connected to voice channel: '{channel}'")

    @app_commands.command(name="play", description="Play Youtube (Powered by WaveLink)")
    @app_commands.describe(search="Search for song")
    async def play(self, interaction: discord.Interaction, search: str):
        if not interaction.guild.voice_client:
          if interaction.user.voice is None:
            return await interaction.response.send_message(f"{interaction.user.mention} Your not connected to a voice, connect it!")
          else:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player())
        elif interaction.user.voice is None:
            return await interaction.response.send_message(f"{interaction.user.mention} Your not connected to a voice, connect it!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        # detect if user put url instead of title
        await interaction.response.defer(thinking=True)
        if re.fullmatch("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", search):
            scsong = (await wavelink.NodePool.get_connected_node().get_tracks(query=search, cls=wavelink.YouTubeTrack))[0]
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
            track = await wavelink.YouTubeTrack.search(search, return_first=False)
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
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player())
        elif interaction.user.voice is None:
            return await interaction.response.send_message(f"{interaction.user.mention} Your not connected to a voice, connect it!")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

       # detect if user put url instead of title
        await interaction.response.defer(thinking=True)
        if re.fullmatch("(?:https?:\/\/)((?:www\.)|(?:m\.))?soundcloud\.com\/[a-z0-9](?!.*?(-|_){2})[\w-]{1,23}[a-z0-9](?:\/.+)?$/?", search):
            scsong = (await wavelink.NodePool.get_connected_node().get_tracks(query=search, cls=wavelink.SoundCloudTrack))[0]
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
            track = await wavelink.SoundCloudTrack.search(search, return_first=False)
            if not track:
             await interaction.followup.send("Song not found")
            else:
             await interaction.followup.send(view=MusicSelectView(track, vc, interaction.user.id, (await interaction.original_response()), timeout=30), wait=True)
        setattr(vc, "loop", False)
        vc.chan = interaction.channel

    @app_commands.command(name="pause", description="Pause song")
    async def pause(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.response.send_message(f"Music paused by {interaction.user.mention}")

    @ app_commands.command(name="resume", description="Resume playing")
    async def resume(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.response.send_message(f"Music is resumed by  {interaction.user.mention}")

    @ app_commands.command(name="stop", description="Stop Player")
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.stop()
        vc.queue.clear()
        await interaction.response.send_message(f"{interaction.user.mention} stopped the music and cleared the queue.")

    @ app_commands.command(name="disconnect", description="Disconnect the Bot from VC")
    async def disconnect(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}, the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.response.send_message(f"{interaction.user.mention} send me out :(")

    @ app_commands.command(name="loop", description="Loops the song")
    async def loop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
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
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
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
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if volume > 300:
            await vc.set_volume(300)
            embed = discord.Embed(
                title=" ", description=f"Volume has been set to {vc.volume}")
            return await interaction.response.send_message(embed=embed)

        await vc.set_volume(volume)
        embed = discord.Embed(
            title=" ", description=f"Volume has been set to {vc.volume}")
        return await interaction.followup.send(embed=embed)

    @app_commands.command(name="nowplaying", description="Show what playing")
    async def playing(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if not vc.is_playing():
            return await interaction.response.send_message("Nothing is playing")

        em = discord.Embed(
            title=f" ", description=f"Playing \n **[{vc.current.track}]({vc.current.uri})** \n Artist: {vc.current.author}")
        em.set_author(name="Now Playing♪", icon_url=f"{self.bot.user.avatar.url}")
        print(vc.current.thumbnail)
        if vc.current.thumbnail is None:
            em.set_thumbnail(
                url="https://media.discordapp.net/attachments/977216545921073192/1033304783156690984/images2.jpg")
        else:
            em.set_thumbnail(url=vc.current.thumbnail)
        bar = progressBar.splitBar(
            int(vc.current.length), int(vc.position), size=10)
        em.add_field(name="Position", value=f"{bar[0]}")
        em.add_field(name="ㅤ", value="ㅤ")
        em.add_field(name="Position",
                     value=f"`{datetime.timedelta(seconds=vc.position)}`")
        em.add_field(name="Duration",
                     value=f"`{datetime.timedelta(seconds=vc.current.length)}`")
        em.set_footer(icon_url=f"{interaction.user.avatar.url}",
                      text=f"Requested by {interaction.user}")
        return await interaction.response.send_message(embed=em)

    @app_commands.command(name="skip", description="Skip a song")
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = discord.Embed(
            title=" ", description=f"[{vc.current.title}]({vc.current.uri}) has been skipped", color=discord.Color.from_rgb(0, 255, 0))
        await interaction.response.send_message(embed=embed)
        await vc.stop()

    @app_commands.command(name="qremove", description="Remove amount of queue")
    async def qremove(self, interaction: discord.Interaction, index: int):
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
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
            return await interaction.response.send_message(f"Hey {interaction.user.mention}the bot are not connected to a voice channel")
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.response.send_message(f"{interaction.user.mention} first you need to join a voice channel")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

            vc.queue.clear()
        return await interaction.response.send_message(f"{interaction.user.mention} cleared the queue.")


async def node_connect(bot):
    await wavelink.NodePool.connect(client=bot, nodes=[wavelink.Node(uri="http://lavalink.clxud.pro:2333", password="youshallnotpass", use_http=True)])
async def setup(bot):
    await bot.loop.create_task(node_connect(bot))
    await bot.add_cog(Music(bot))
