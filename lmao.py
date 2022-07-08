import ast
import urllib
import typing
from discord import app_commands
from discord import ClientException
import re
import os
import subprocess
import math
import functools
import sys
import io
from lyricsgenius import Genius
import inspect
import random
import discord
from discord.ext import commands
from discord.ext import tasks
import json
from botmod import bypass
import youtube_dl
import aiohttp
import asyncio
import time
import datetime
import platform

from wavelink import (LavalinkException, LoadTrackError, SoundCloudTrack,
                      YouTubeMusicTrack, YouTubePlaylist, YouTubeTrack)
from wavelink.ext import spotify
from wavelink.ext.spotify import SpotifyTrack

from utilities._classes import Provider
from utilities.checks import voice_channel_player, voice_connected
from utilities.errors import MustBeSameChannel
from utilities.paginator import Paginator
from utilities.player import DisPlayer

import requests
from enum import Enum
import lavalink
from dotenv import load_dotenv
from discord.utils import get
from discord import NotFound
import akinator
import itertools
from async_timeout import timeout
from discord.gateway import DiscordWebSocket, _log
from akinator.async_aki import Akinator
from json import loads
import wavelink
import async_timeout

load_dotenv()

genius = Genius()

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents)

#


@bot.event
async def on_ready():
 print("Logged As")
 print(f"@{bot.user.name}#{bot.user.discriminator}")
 print("Registering Commands (Wont take long time)....")
 await bot.add_cog(Music(bot))
 await bot.add_cog(Fun(bot))
 await bot.add_cog(Moderation(bot))
 await bot.add_cog(Other(bot))
 await bot.add_cog(Owner(bot))
 await bot.add_cog(nsfw(bot))
 print("Powered by dismusic")

@bot.event
async def on_member_join(member):
       embed = discord.Embed(title=f"Welcome to {member.guild.name}, {member.name}!", description="By Joining, Your agree to the rules given in server")
       embed.timestamp = datetime.datetime.now()
       await member.send(embed=embed)

@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send(f"Hello {message.author.mention}, My prefix is {bot.command_prefix}")
    else:
        await bot.process_commands(message) # This line makes your other commands work.

@bot.event
async def on_connect():
      await bot.change_presence(activity=discord.Game(name="First Release: Codename : Captain Opstober"))

"""
ZairullahDeveloper once said: Being a developer isnt that easy, start from making mistakes
"""

class MyHelpCommand(commands.MinimalHelpCommand):

 async def send_pages(self):
  destination = self.get_destination()
  for command in bot.commands:
   embed=discord.Embed(title="Alexandra ", url="https://discord.com/api/oauth2/authorize?client_id=972459217548099584&permissions=0&scope=bot%20applications.commands", description="")
   embed.set_author(name="ZairullahDeveloper", url="https://github.com/zairullahdev", icon_url="https://i.ibb.co/9q6MYnM/Png.png")
   embed.set_thumbnail(url="https://camo.githubusercontent.com/51f16d28861eade2210bb6c5414a1d6b0096d0d8d56debc5fc64e8b88681c154/68747470733a2f2f656e637279707465642d74626e302e677374617469632e636f6d2f696d616765733f713d74626e3a414e6439476354664f54472d6d5268655674414b7164366430613774522d7157716b534e75464869767726757371703d434155")
   embed.add_field(name='By OrdinaryEnder Feat ZairullahDeveloper', value='MIT License')
   embed.set_footer(text="Any suggestions contact ZairullahDeveloper in GitHub (zairullahdev)")
  for page in self.paginator.pages:
            embed.description += page
  await destination.send(embed=embed)

bot.help_command = MyHelpCommand()

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
     self.bot = bot
     super().__init__()
 
    @commands.command(name='lvbypass', description='Bypass Linkvertise (powered by bypass.vip)')
    async def _lvbypass(self, ctx, url):
       link = bypass(url)
       loadlink = json.dumps(link)
       finalink = json.loads(loadlink)
       print(finalink)
       datalink = finalink.get("destination")
       embed=discord.Embed(title="Result", description="Dont let your data get sold by Them!")
       embed.add_field(name="ㅤ", value=datalink)
       await ctx.send(embed=embed)


    @commands.command(name='8ball', description='Let the 8 Ball Predict!\n')
    async def _8ball(self, ctx, *, question: str):
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
             'I am tired. *proceeds with sleeping*']
     response = random.choice(responses)
     embed=discord.Embed(title="The Magic 8 Ball has Spoken!")
     embed.add_field(name='Question: ', value=f'{question}', inline=True)
     embed.add_field(name='Answer: ', value=f'{response}', inline=False)
     await ctx.send(embed=embed)


    @commands.command(name='akinator', description="Lemme guess ur character")
    async def akinator(self, ctx):
     await ctx.send("Akinator is here to guess!")
     def check(msg):
         return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n","p","b"]
     try:
         aki = akinator.Akinator()
         q = aki.start_game()
         while aki.progression < 80:
             await ctx.send(q)
             await ctx.send("Your answer:(y/n/p/b)")
             msg = await bot.wait_for("message", check=check)
             if msg.content.lower() == "b":
                 try:
                     q=aki.back()
                 except aki.CantGoBackAnyFurther:
                     await interaction.response.send_message(e)
                     continue
             else:
                 try:
                     q = aki.answer(msg.content.lower())
                 except aki.InvalidAnswerError as e:
                     await interaction.response.send_message(e)
                     continue
         aki.win()
         await ctx.send(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?(y/n)\n{aki.first_guess['absolute_picture_path']}\n\t")
         correct = await bot.wait_for("message", check=check)
         if correct.content.lower() == "y":
             await interaction.response.send_message("Yay\n")
         else:
             await interaction.response.send_message("Oof\n")
     except Exception as e:
         await interaction.response.send_message(e)
    
    @commands.command(name="date", description="Show today date")
    async def __date(self, ctx):
     date = datetime.datetime.now().strftime("%Y-%m-%d")
     time = datetime.datetime.now().strftime("%H:%M:%S")
     embed=discord.Embed(title="Now", description=f"Today is")
     embed.add_field(name="Date", value=date)
     embed.add_field(name="Time", value=time)
     embed.set_footer(text="If you wanna donate to us your can execute donate command")
     await ctx.send(embed=embed)

    @commands.command(name="math", description="Math")
    async def __math(self, ctx, num1: float, op: str, num2: float):
     if op == "+":
      result = num1 + num2
     elif op == "-":
      result = num1 - num2
     elif op == "*":
      result =num1 * num2
     elif op == "/":
      result = num1 / num2
      
     embed = discord.Embed(title="Result", description="ㅤ", color=discord.Color.from_rgb(0, 0, 0))
     embed.add_field(name="Result Of Your Math:", value=f"{num1} {op} {num2} = {result}")
     embed.set_footer(text="Be Smart Next Time!")
     await ctx.send(embed=embed)

    @commands.command(name="meme", description="Reddit Memes")
    async def meme(self, ctx):
      async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed=discord.Embed(title="Memes", description=" ")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])

            await ctx.send(embed=embed)
    @commands.command(name="typerace", description="Lets see how fast your typing")
    async def typerace(self,  message):
        ##  no need for bot to reply to itself
        
            answer = 'Linux is a family of open-source Unix-like operating systems based on the Linux kernel, an operating system kernel first released on September 17, 1991, by Linus Torvalds. Linux is typically packaged in a Linux distribution.'
            timer  = 10.5
            await message.channel.send(f'You have {timer} seconds to type:  {answer}')

            def is_correct(msg):
                return msg.author == message.author

            try:
                guess = await bot.wait_for('message',  check=is_correct,  timeout=timer)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long.')

            if guess.content == answer:
                await message.channel.send('Right on!')
            else:
                await message.channel.send('Oops.')

    @commands.command(name="linusquotes", description="Get Better Motivation from Linus Torvalds!")
    async def quotes(self, ctx):
     r = requests.get("https://linusquote.com/quote")
     load = r.json()
     jsonload = json.dumps(load)
     final = json.loads(jsonload)
     print(final['body'])
     embed = discord.Embed(title="Linus Torvalds Once Said:", description="ㅤ")
     embed.add_field(name="ㅤ", value=f"{final['body']}")
     await ctx.send(embed=embed)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
     await ctx.send("ALT+F4 PRESSED")

     await ctx.send("Bye :(")
     await bot.close()

    @commands.command(name='shell', description='Console Remote')
    @commands.is_owner()
    async def _eval(self, ctx, *, cmd):
        # Ender : This very  damger dont give it to your friend ig D:<
        await ctx.send(f"Current Shell = {os.getenv('SHELL')}")
        results = subprocess.check_output(cmd, shell=True)
        lmao = results.decode("utf-8")

        await ctx.send(f"```css\n{ lmao }```")

    @commands.command(name='restart', description='Restart Bot Session')
    @commands.is_owner()
    async def _restart(self, ctx):
          embed = discord.Embed(title="Restarting.....", description="")
          embed.set_thumbnail(url="https://camo.githubusercontent.com/51f16d28861eade2210bb6c5414a1d6b0096d0d8d56debc5fc64e8b88681c154/68747470733a2f2f656e637279707465642d74626e302e677374617469632e636f6d2f696d616765733f713d74626e3a414e6439476354664f54472d6d5268655674414b7164366430613774522d7157716b534e75464869767726757371703d434155")
          embed.add_field(name="<a:igloading:989097955619393546>", value="Give us a support in [Github!](https://github.com/zairullahdev/Alexandra)")
          embed.timestamp = datetime.datetime.now()
          await ctx.send(embed=embed)
          await asyncio.sleep(3)
          await ctx.channel.purge(limit=1)
          restart_bot()

    @commands.command(name='chpresence', description='Change Bot Presence As You Wanted')
    @commands.is_owner()
    async def _chp(self, ctx, type, *, name=None, twittch=None):
          if type == 'playing':
             await bot.change_presence(activity=discord.Game(name=name))
          elif type == 'watching':
             await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
          elif type == 'listening':
             await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
          elif type == 'streaming':
             await bot.change_presence(activity=discord.Streaming(name=name, url=twittch))
          elif type == 'sleep':
             await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name = '24/7 Lo-fi'))
    @commands.command(name="eval", description="Quick Eval")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
     codexec = await eval(code)
     await ctx.send(f"```py\n { codexec } \n```")

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', description='Kick Dumbass from Your Holy Server')
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, Member: discord.Member):
        if ctx.author.top_role < user.top_role:
                return await ctx.send("**You don't have enough permission**")
        if ctx.author.top_role > user.top_role:
                return await bot.kick(Member)
                return await ctx.send(f"{user} Successfully Banned by {ctx.author.mention}")
    @_kick.error
    async def kick_error(ctx, error):
     if isinstance(error, discord.ext.commands.BadArgument):
        await bot.say('Could not recognize user')

    @commands.command(name='ban', description='Ban dumbass from your Holy Server')
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, user: discord.Member, *, reason=None):
        if reason == None:
           reason = f"{user} banned by {ctx.author}"
        if ctx.author.top_role < user.top_role:
           return await ctx.send("**You don't have enough permission**")
        if ctx.author.top_role > user.top_role:
           return await ctx.guild.ban(user, reason=reason)
           return await ctx.send(f"{user} Successfully Banned by {ctx.author.mention}")

    @commands.command(name='unban', description='Unban people who have repented')
    @commands.has_permissions(ban_members=True)
    async def _unban(ctx, id: int):
         user = await bot.fetch_user(id)
         await ctx.guild.unban(user)

    @commands.command(name='mute', description='Mute Whos Keep Spamming on ur Holy Server', pass_context = True)
    @commands.has_permissions(manage_messages=True)
    async def _mute(self, ctx, member: discord.Member, time, *, reason=None):
            mutedrole = os.getenv("MUTED_ROLE")
            mutedRole = discord.utils.get(ctx.guild.roles, name=mutedrole)
            memrole = os.getenv("MEMBER_ROLE")
            guild = ctx.guild
            memberrole = discord.utils.get(ctx.guild.roles, name=memrole)
            time_convert = {"s":1, "m":60, "h":3600, "d":86400, "w":604800, "mo":18144000, "y":31536000}
            tempmute= int(time[:-1]) * time_convert[time[-1]]
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                embed = discord.Embed(title="Muted!", description=f"{member.mention} was muted   for {time}, dont leave the server or you'll get banned! ", colour=discord.Colour.light_gray())
                embed.add_field(name="Reason:", value=reason, inline=True)
                await ctx.send(embed=embed)
                await member.add_roles(mutedRole, reason=reason)
                await asyncio.sleep(tempmute)
                await member.send(f"You have been unmuted from {guild.name}, Dont break rules again!")
                await member.remove_roles(mutedRole)
                break



    @commands.command(name='unmute', description='Unmute')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
         mutedRole = discord.utils.get(ctx.guild.roles, name="Nameless Muted")
         memberrole = discord.utils.get(ctx.guild.roles, name="Nameless Member")

         await member.remove_roles(mutedRole)
         await member.send(f" you have unmutedd from: - {ctx.guild.name}")
         embed = discord.Embed(title="Unmuted", description=f" Unmuted {member.mention}")
         await member.add_roles(memberrole)
         await ctx.send(embed=embed)
       
    @commands.command(name='purge', description='Purge Old Messages', pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def _purge(self, ctx, limit: int):
         await ctx.channel.purge(limit=limit)
         await ctx.send("Purged by {}".format(ctx.author.mention), delete_after=5)
         await ctx.message.delete()

    @commands.command(name='nick', description='Change Nickname of people')
    @commands.has_permissions(manage_nicknames=True)
    async def chnick(self, ctx, member: discord.Member, *, nick):
     await member.edit(nick=nick)
     await ctx.send(f'Nickname was changed for {member.mention} ')


class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='image', description='Get Images')
    @commands.is_nsfw()
    async def _image(self, ctx, image):
     img = image
     r = requests.get("https://nekos.life/api/v2/img/{}".format(image))
     res = r.json()
     em = discord.Embed()
     em.set_image(url=res['url'])
     await ctx.send(embed=em)

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='avatar', description='get someone avatar (avatar copy)')
    async def _avatar(self, ctx, avamember : discord.Member):
       userAvatarUrl = avamember.avatar.url
       await ctx.send(userAvatarUrl)

    @commands.command(name='say', description='say smth')
    async def _speak(self, ctx, *, text):
     message = ctx.message
     await message.delete()

     await ctx.send(f"{text}")

    @commands.command(name='robloxinfo', description='Get Roblox Game Info')
    async def _robloxinfo(self, ctx, *, placeid):
   # First we gonna get Universe ID, Because Roblox Only Allow show game with it
     uidget = requests.get('https://api.roblox.com/universes/get-universe-containing-place?placeid={}'.format(placeid))
     universeload = uidget.json()
     load = json.dumps(universeload)
     getid = json.loads(load)
# and finally, post your universe id into roblox
     robloxgame = requests.get('https://games.roblox.com/v1/games?universeIds={}'.format(getid['UniverseId']))
     returngame = robloxgame.json()
     getinfogame = json.dumps(returngame, indent=4, sort_keys=True)
  # send it as json because this is for developer
     jsonroblox = '```'
     await ctx.send(f'```json\n{ getinfogame }\n```')

    @commands.command(name='upload', description='Upload Files Into transfer.sh')
    async def upfile(self, ctx):
     bonk = ctx.message.attachments[0]
     url = bonk.url
     local_filename = url.split('/')[-1]
     # NOTE the stream=True parameter below
     with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
     files = {'file': open(local_filename, 'rb')}
     up = requests.post('https://transfer.sh', files=files)
     print(up.text)
     embed = discord.Embed(title='Result', description=up.text)
     embed.set_footer(text="Powered by https://transfer.sh")
     await ctx.send(embed=embed)
     # Because it already done lets remove it
     os.remove(local_filename)

    @commands.command(name="donate", description="Donate using PayPal (Indonesia Only)")
    async def donate(self, ctx):
     embed=discord.Embed(title="Donate", description="")
     embed.set_image(url="https://i.ibb.co/pn6LLZj/Donation.png")
     await ctx.send(embed=embed)

    @commands.command(name="ping", description="Pong! <3")
    async def ping(self, ctx):
          await ctx.send(f"Pong!\nLatency: {bot.latency}")

    @commands.command(name="search", description="Search Youtube Videos")
    async def yt(self, ctx, *, search):
     query_string = urllib.parse.urlencode({
        "search_query": search
     })
     html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
     )
     search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
     await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])

class Music(commands.Cog):
    """Music commands"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.start_nodes())

    def get_nodes(self):
        return sorted(wavelink.NodePool._nodes.values(), key=lambda n: len(n.players))

    async def play_track(self, ctx: commands.Context, query: str, provider=None):
        player: DisPlayer = ctx.voice_client

        if ctx.author.voice.channel.id != player.channel.id:
            raise MustBeSameChannel(
                "You must be in the same voice channel as the player."
            )

        track_providers = {
            "yt": YouTubeTrack,
            "ytpl": YouTubePlaylist,
            "ytmusic": YouTubeMusicTrack,
            "soundcloud": SoundCloudTrack,
            "spotify": SpotifyTrack,
        }

        query = query.strip("<>")
        msg = await ctx.send(f"Searching for `{query}` :mag_right:")

        track_provider = provider if provider else player.track_provider

        if track_provider == "yt" and "playlist" in query:
            provider = "ytpl"

        provider: Provider = (
            track_providers.get(provider)
            if provider
            else track_providers.get(player.track_provider)
        )

        nodes = self.get_nodes()
        tracks = list()

        for node in nodes:
            try:
                with async_timeout.timeout(20):
                    tracks = await provider.search(query, node=node)
                    break
            except asyncio.TimeoutError:
                self.bot.dispatch("dismusic_node_fail", node)
                wavelink.NodePool._nodes.pop(node.identifier)
                continue
            except (LavalinkException, LoadTrackError):
                continue

        if not tracks:
            return await ctx.send("No song/track found with given query.")

        if isinstance(tracks, YouTubePlaylist):
            tracks = tracks.tracks
            for track in tracks:
                await player.queue.put(track)

            await msg.edit(content=f"Added `{len(tracks)}` songs to queue. ")
        else:
            track = tracks[0]

            await msg.edit(content=f"Added `{track.title}` to queue. ")
            await player.queue.put(track)

        if not player.is_playing():
            await player.do_next()

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        spotify_credential = getattr(
            self.bot, "spotify_credentials", {"client_id": "", "client_secret": ""}
        )

        for config in self.bot.lavalink_nodes:
            try:
                node: wavelink.Node = await wavelink.NodePool.create_node(
                    bot=self.bot,
                    **config,
                    spotify_client=spotify.SpotifyClient(**spotify_credential),
                )
                print(f"[dismusic] INFO - Created node: {node.identifier}")
            except Exception:
                print(
                    f"[dismusic] ERROR - Failed to create node {config['host']}:{config['port']}"
                )

    @commands.command(aliases=["con"])
    @voice_connected()
    async def connect(self, ctx: commands.Context):
        """Connect the player"""
        if ctx.voice_client:
            return

        msg = await ctx.send(f"Connecting to **`{ctx.author.voice.channel}`**")

        try:
            player: DisPlayer = await ctx.author.voice.channel.connect(cls=DisPlayer)
            self.bot.dispatch("dismusic_player_connect", player)
        except (asyncio.TimeoutError, ClientException):
            return await msg.edit(content="Failed to connect to voice channel.")

        player.bound_channel = ctx.channel
        player.bot = self.bot

        await msg.edit(content=f"Connected to **`{player.channel.name}`**")

    @commands.group(aliases=["p"], invoke_without_command=True)
    @voice_connected()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play or add song to queue (Defaults to YouTube)"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query)

    @play.command(aliases=["yt"])
    @voice_connected()
    async def youtube(self, ctx: commands.Context, *, query: str):
        """Play a YouTube track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "yt")

    @play.command(aliases=["ytmusic"])
    @voice_connected()
    async def youtubemusic(self, ctx: commands.Context, *, query: str):
        """Play a YouTubeMusic track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "ytmusic")

    @play.command(aliases=["sc"])
    @voice_connected()
    async def soundcloud(self, ctx: commands.Context, *, query: str):
        """Play a SoundCloud track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "soundcloud")

    @play.command(aliases=["sp"])
    @voice_connected()
    async def spotify(self, ctx: commands.Context, *, query: str):
        """play a spotify track"""
        await ctx.invoke(self.connect)
        await self.play_track(ctx, query, "spotify")

    @commands.command(aliases=["vol"])
    @voice_channel_player()
    async def volume(self, ctx: commands.Context, vol: int, forced=False):
        """Set volume"""
        player: DisPlayer = ctx.voice_client

        if 0 <= vol <= 300:                              
         if player.is_playing():                          
            new_volume = vol / 100                   
            player.source.volume = vol
            await ctx.send(f"Volume set to {vol} :loud_sound:")

    @commands.command(aliases=["disconnect", "dc"])
    @voice_channel_player()
    async def stop(self, ctx: commands.Context):
        """Stop the player"""
        player: DisPlayer = ctx.voice_client

        await player.destroy()
        await ctx.send("Stopped the player :stop_button: ")
        self.bot.dispatch("dismusic_player_stop", player)

    @commands.command()
    @voice_channel_player()
    async def pause(self, ctx: commands.Context):
        """Pause the player"""
        player: DisPlayer = ctx.voice_client

        if player.is_playing():
            if player.is_paused():
                return await ctx.send("Player is already paused.")

            await player.set_pause(pause=True)
            self.bot.dispatch("dismusic_player_pause", player)
            return await ctx.send("Paused :pause_button: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def resume(self, ctx: commands.Context):
        """Resume the player"""
        player: DisPlayer = ctx.voice_client

        if player.is_playing():
            if not player.is_paused():
                return await ctx.send("Player is already playing.")

            await player.set_pause(pause=False)
            self.bot.dispatch("dismusic_player_resume", player)
            return await ctx.send("Resumed :musical_note: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def skip(self, ctx: commands.Context):
        """Skip to next song in the queue."""
        player: DisPlayer = ctx.voice_client

        if player.loop == "CURRENT":
            player.loop = "NONE"

        await player.stop()

        self.bot.dispatch("dismusic_track_skip", player)
        await ctx.send("Skipped :track_next:")

    @commands.command()
    @voice_channel_player()
    async def seek(self, ctx: commands.Context, seconds: int):
        """Seek the player backward or forward"""
        player: DisPlayer = ctx.voice_client

        if player.is_playing():
            old_position = player.position
            position = old_position + seconds
            if position > player.source.length:
                return await ctx.send("Can't seek past the end of the track.")

            if position < 0:
                position = 0

            await player.seek(position * 1000)
            self.bot.dispatch("dismusic_player_seek", player, old_position, position)
            return await ctx.send(f"Seeked {seconds} seconds :fast_forward: ")

        await ctx.send("Player is not playing anything.")

    @commands.command()
    @voice_channel_player()
    async def loop(self, ctx: commands.Context, loop_type: str = None):
        """Set loop to `NONE`, `CURRENT` or `PLAYLIST`"""
        player: DisPlayer = ctx.voice_client

        result = await player.set_loop(loop_type)
        await ctx.send(f"Loop has been set to {result} :repeat: ")

    @commands.command(aliases=["q"])
    @voice_channel_player()
    async def queue(self, ctx: commands.Context):
        """Player queue"""
        player: DisPlayer = ctx.voice_client

        if len(player.queue._queue) < 1:
            return await ctx.send("Nothing is in the queue.")

        paginator = Paginator(ctx, player)
        await paginator.start()

    @commands.command(aliases=["np"])
    @voice_channel_player()
    async def nowplaying(self, ctx: commands.Context):
        """Currently playing song information"""
        player: DisPlayer = ctx.voice_client
        await player.invoke_player(ctx)
    
    @commands.command(name='lyrics', description='Genius Lyrics')
    async def lyrics(self, ctx, artist, *, title):
     try:
      song = genius.search_song(title, artist)
      lyric = song.lyrics
      print(lyric[:lyric.rfind("Embed")])
      embedgenius = discord.Embed(title=f"{song.title} by {song.artist}", description=f"\n{lyric[:lyric.rfind('Embed')]}")
      await ctx.send(embed=embedgenius)
     except Exception as e:
      await ctx.send(f"Something wrong, Report this to !        from ender import bot#2105\n Logs: \n ```py\n{e}\n```")

bot.lavalink_nodes = [
    {"host": "lava.link", "port": 80, "password": "dismusic"},
    {"host": "lavalink-with-replit.endergaming3.repl.co", "port":443, "password": "youshallnotpass", "https": True}
]

token = os.getenv("TOKEN")


bot.run(token)
