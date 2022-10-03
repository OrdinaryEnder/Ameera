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
from wavelink import Node as node
from mod.botmod import bypass
import youtube_dl
import aiohttp
import asyncio
import time
import datetime
import datetime as dt
import typing as t
from email.base64mime import body_encode
import wavelink

from enum import Enum
import lavalink
from dotenv import load_dotenv
from discord.utils import get
from discord import NotFound
import itertools
from async_timeout import timeout
from discord.gateway import DiscordWebSocket, _log
from json import loads
import wavelink
import async_timeout

load_dotenv()
colorama.init(autoreset=True)

genius = Genius()
# this is will cached
def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

# setup hook
class MyBot(commands.Bot):
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

  async def setup_hook(self):
   print(Fore.BLUE + "Registering Commands (Wont take long time)....")
   print(Fore.YELLOW + Fore.RED + "Adding Music cogs")
   await bot.add_cog(Music(bot))
   await node_connect(bot)
   print(Fore.GREEN + "Adding Fun Cogs")
   await bot.add_cog(Fun(bot))
   print(Fore.BLUE + "Adding Moderation Cogs ")
   await bot.add_cog(Moderation(bot))
   print(Fore.MAGENTA + "Adding Other Cogs")
   await bot.add_cog(Other(bot))
   print(Fore.YELLOW + "Adding Owner Cogs")
   await bot.add_cog(Owner(bot))
   print(Fore.RED + "Adding Nsfw Cogs")
   await bot.add_cog(nsfw(bot))
   print(Back.WHITE + Fore.RED + "Support" + Fore.YELLOW + " us" + Fore.BLUE + " at" + Fore.GREEN + " https://github.com/OrdinaryEnder/Olivia")
   global startTime
   startTime = time.time()




intents = discord.Intents().all()
bot = MyBot(command_prefix='+', intents=intents, activity=discord.Game(name="wassup"))


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
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
      return await vc.play(track)

    try:
      next_song = vc.queue.get()
      await vc.play(next_song)
      embed = discord.Embed(title=" ", description=f"Started playing  **[{next_song.title}]({next_song.uri})**")
      await ctx.send(embed=embed)
    except wavelink.errors.QueueEmpty:
      embed = discord.Embed(title=" ", description="There are no more tracks", color=discord.Color.from_rgb(255, 0, 0))
      await ctx.send(embed=embed)
      await vc.disconnect()

@bot.event
async def on_ready():
 print(Back.RED + Fore.BLACK + "Logged As")
 print(Back.WHITE + Fore.BLACK + f"@{bot.user.name}#{bot.user.discriminator}")

@bot.event
async def on_member_join(member):
       embed = discord.Embed(title=f"Welcome to {member.guild.name}, {member.name}!", description="By Joining, Your agree to the rules given in server")
       embed.timestamp = datetime.datetime.now()
       await member.send(embed=embed)
       await member.add_roles(member.guild.get_role(os.getenv("MEMBER_ROLE")))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)
    return

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
  for command in bot.commands:
   embed=discord.Embed(title="Alexandra ", url="https://discord.com/api/oauth2/authorize?client_id=972459217548099584&permissions=0&scope=bot%20applications.commands", description="")
   embed.set_author(name="ZairullahDeveloper", url="https://github.com/zairullahdev", icon_url="https://i.ibb.co/gD6mLh7/Png.png")
   embed.set_thumbnail(url="https://i.ibb.co/fp247vT/Untitled1-20220728065509.png")
   embed.add_field(name='By OrdinaryEnder Feat ZairullahDeveloper', value='GPL-2.0 License')
   embed.set_footer(text="Any suggestions contact ZairullahDeveloper in GitHub (zairullahdev)")
  for page in self.paginator.pages:
            embed.description += page
  await destination.send(embed=embed)

# slash support of help
bot.help_command = MyHelpCommand()

# music view
class MusicDropDown(discord.ui.Select):
    def __init__(self, track):
      ret = []
      for song in track[:5]:
          ret.append(discord.SelectOption(label=song.title, description=song.author, value=song.uri))

          options = ret

      super().__init__(placeholder='Choose song ...', min_values=1, max_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        search = (await node.get_tracks(wavelink.SoundCloudTrack, self.values[0]))
        if vc.queue.is_empty and not vc.is_playing():
         await vc.play(search)
         embed = discord.Embed(title="Now playing", description=f"[{search.title}]({search.uri})\n \n Uploader: {search.author}")
         embed.set_thumbnail(url=search.thumbnail)
         embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
         await self.message.edit(embed=embed, view=None)
        else:
         await vc.queue.put_wait(search)
         await self.message.edit(f"Added {search.title} to the queue", view=None)
        vc.ctx = ctx
        setattr(vc, "loop", False)


class MusicSelectView(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.add_item(MusicDropDown(self.track))




# meme view
class refreshbutton(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.value = None

    async def on_timeout(self):
        for butt in self.children:
            butt.disabled = True


        await self.message.edit(view=self)
    # part of slash move, this is cool.
    @discord.ui.button(label="🔄", style=discord.ButtonStyle.grey)
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
     pages=["memes",
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
            embed=discord.Embed(title="Daily Memes", description=" ")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await interaction.response.edit_message(embed=embed)

 

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
     self.bot = bot
     super().__init__()
 
    @app_commands.command(name='lvbypass', description='Bypass Linkvertise (powered by bypass.vip)')
    @app_commands.describe(url="URL About to Bypass (Example: https://linkvertise.com/38666/ArceusXRoblox")
    async def _lvbypass(self, interaction: discord.Interaction, url: str):
       link = await bypass(url)
       loadlink = json.dumps(link)
       finalink = json.loads(loadlink)
       print(finalink)
       datalink = finalink.get("destination")
       embed=discord.Embed(title="Result", description="Dont let your data get sold by Them!")
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
     embed=discord.Embed(title="The Magic 8 Ball has Spoken!")
     embed.add_field(name='Question: ', value=f'{question}', inline=True)
     embed.add_field(name='Answer: ', value=f'{response}', inline=False)
     await interaction.response.send_message(embed=embed)


    @app_commands.command(name='akinator', description="Lemme guess ur character")
    async def akinator(self, interaction: discord.Interaction):
        await interaction.response.send_message("Akinator is disabled for some reason \n Reason: deprecated", ephemeral=True)
     
      
    @app_commands.command(name="math", description="Math")
    @app_commands.describe(num="Needed number", operation="+ for summation ,- for subtraction , * for multiplication, / for divine", num2="another number")
    async def math(self, interaction: discord.Interaction, num: int, operation: str, num2: int):
     if operation not in ['+', '-', '*', '/']:
         await ctx.send('Please type a valid operation type. (+ for summation ,- for subtraction , * for multiplication, ÷ for divine)')
     var = f'{num} {operation} {num2}'
     embed = discord.Embed(title="Result", description="ㅤ", color=discord.Color.from_rgb(0, 0, 0))
     embed.add_field(name="Result Of Your Math:", value=f"{var} = {eval(var)}")
     embed.set_footer(text="Be Smart Next Time!")
     await interaction.response.send_message(embed=embed)

    @app_commands.command(name="meme", description="Reddit Memes")
    async def meme(self, interaction: discord.Interaction):
      pages=["memes",
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
            embed=discord.Embed(title="Daily Memes", description=" ")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])

            view = refreshbutton(timeout=30.0)
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
          embed = discord.Embed(title="Linus Torvalds Once Said:", description="ㅤ")
          embed.add_field(name="ㅤ", value=f"{final['body']}")
          await interaction.response.send_message(embed=embed)

    @app_commands.command(name="qrgen", description="Generates QR using Data (Can be URL or Anything")
    @app_commands.describe(data="URL Or String")
    async def qrgen(self, interaction: discord.Interaction, data: str):
     await interaction.response.defer(ephemeral=True)
     img = qrcode.make(data)
     img.save("temp.png")
     embed = discord.Embed(title="Successfully Generated", description="Result")
     file = discord.File("temp.png", filename="image.png")
     embed.set_image(url="attachment://image.png")
     await interaction.followup.send(embed=embed, file=file)
     os.remove("temp.png")

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gcclean")
    @commands.is_owner()
    async def gc(self, ctx):
     await ctx.send(f"Cleaned {gc.collect()} Garbage Collections")

    @commands.command(name="shutdown", description="Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
     await ctx.send("ALT+F4 PRESSED")

     await ctx.send("Bye :(")
     await bot.close()

    @commands.command(name='shell', description='Console Remote')
    @commands.is_owner()
    @app_commands.describe(cmd="The Command About to executed in shell")
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
          await ctx.channel.purge(limit=1, check=lambda m: m.author == bot.user)
          restart_bot()

    @commands.command(name='chpresence', description='Change Bot Presence As You Wanted')
    @commands.is_owner()
    async def _chp(self, ctx, type, *, name, twittch=None):
          if type == 'playing':
             await bot.change_presence(activity=discord.Game(name=name))
             await ctx.send(f"Lets play {name}")
          elif type == 'watching':
             await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
             await ctx.send(f"Time to watch {name}")
          elif type == 'listening':
             await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
             await ctx.send("🎶🎶🎶")
          elif type == 'streaming':
             await bot.change_presence(activity=discord.Streaming(name=name, url=twittch))
             await ctx.send(f"Lets stream {name}")
          elif type == 'sleep':
             await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name = '24/7 Lo-fi'))
             await ctx.send("zzz")
            
    @commands.command(name="eval", description="Quick Eval (Codeblock)") 
    @commands.is_owner()
    async def eval(self, ctx, *, code):
     try:
      if "```" in code:
       content = re.sub("```python|```py|```", "", code)
       codexec = exec(content)
       embed = discord.Embed(title="Eval", description=" ")
       embed.add_field(name= " ", value=f"```py\n { codexec } \n```")
       await ctx.send(embed=embed)
      else:
       codexec = exec(code)
       embed = discord.Embed(title="Eval", description=" ")
       embed.add_field(name= " ", value=f"```py\n { codexec } \n```")
       await ctx.send(embed=embed)
     except Exception as e:
         embed = discord.Embed(title="Eval", description=" ")
         embed.add_field(name= " ", value=f"```py\n { e } \n```")
         await ctx.send(embed=embed)

    @commands.command(name="awaiteval", description="Await an eval")
    @commands.is_owner()
    async def awaiteval(self, ctx, *, code):
     try:
      if "```" in code:
       content = re.sub("```python|```py|```", "", code)
       codexec = await eval(content)
       await ctx.send(f"```py\n { codexec } \n```")
      else:
       codexec = await eval(code)
       await ctx.send(f"```py\n { codexec } \n```")
     except Exception as e:
       await ctx.send(f"```css\n { e }\n```")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="had enough?, Mute still annoy u?, Try timeout")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="Valid Member", time="For example, 1d is for 1 day, s for second, m for minutes, h for hour, d for day", reason="The reason")

    async def timeout(self, interaction: discord.Interaction, member: discord.Member, time: str, reason: str = None):
     time_convert = {"s":1, "m":60, "h":3600, "d":86400}
     tempmute= int(time[:-1]) * time_convert[time[-1]]
     await member.timeout(datetime.timedelta(seconds=tempmute), reason=reason)
     embed = discord.Embed(title="Timed out", description=f"Timed out user: {member.mention}\n \n For {time} \n \n Tryna Leave ur still can get timed out haha", color=0xe74c3c)
     await interaction.response.send_message(embed=embed)

    @app_commands.command(name="untimeout", description="Untimeout user")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="Timed out member")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
     await member.timeout(None)
     embed = discord.Embed(title="Untimed out", description=f"Untimed out {member.mention}", color=0x2ecc71)
     await interaction.response.send_message(embed=embed)

    @app_commands.command(name='kick', description='Kick Dumbass from Your Holy Server')
    @app_commands.describe(member="Member About to kicked", reason="Reason")
    @app_commands.checks.has_permissions(kick_members=True)
    async def _kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
                await interaction.guild.kick(Member, reason=reason)
                await interaction.response.send_message(f"{Member} Successfully kicked by {ctx.author.mention}")

    @app_commands.command(name='ban', description='Ban dumbass from your Holy Server')
    @app_commands.describe(user="Member About to banned", reason="Reason")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"Successfully banned {user} by {ctx.author.mention}, reason={reason}")
    @app_commands.command(name='unban', description='Unban people who have repented')
    @app_commands.describe(id="ID of Member About to unban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _unban(self, interaction: discord.Interaction, id: int):
         user = await bot.fetch_user(int(id))
         await interaction.guild.unban(user)
         await interaction.response.send_message(f"Unbanned @{user.name}#{user.discriminator}")
    @app_commands.command(name="idban", description="Ban using ID (For Unfair Leaver")
    @app_commands.describe(id="ID of Member About to banned", reason="Reason")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _idban(self, interaction: discord.Interaction, id: int, reason: str = None):
        user = await bot.fetch_user(int(id))
        await interaction.guild.ban(user, reason=reason)
        await imteraction.response.send_message(f"Banned @{user.name}#{user.discriminator}, Reason = {reason}")
      
    @app_commands.command(name='purge', description='Purge Old Messages')
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(limit="How much ur gonna delete")
    async def _purge(self, interaction: discord.Interaction, limit: int):
        if limit > 100:
            return await interaction.response.send_message("Too much 😖", ephemeral=True)

        messcount = limit + 1
        await interaction.response.defer()
        await interaction.channel.purge(limit=messcount)
        await interaction.followup.send("Purged by {}".format(interaction.user.mention), delete_after=5)

    @app_commands.command(name='nick', description='Change Nickname of people')
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.describe(member="Member", nick="New Nickname")
    async def chnick(self, interaction: discord.Interaction, member: discord.Member, nick: str):
     await member.edit(nick=nick)
     await interaction.response.send_message(f'Nickname was changed for {member.mention} ')


class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="image", description="Get Images (NSFW!!!!!)", nsfw=True)
    @app_commands.describe(image="NSFW Image about to show")
    async def _image(self, interaction: discord.Interaction, image: typing.Literal['hass', 'hmidriff', 'pgif', 'hentai', 'holo', 'hneko', 'neko', 'hkitsune', 'kemonomimi', 'anal', 'hanal', 'gonewild', 'kanna', 'ass', 'pussy', 'thigh', 'hthigh', 'gah', 'coffee', 'food', 'paizuri', 'tentacle', 'boobs', 'hboobs', 'yaoi']):
        try:   
         await interaction.response.defer()
         async with aiohttp.ClientSession() as session:
          async with session.get(f"https://nekobot.xyz/api/image?type={image}") as r:
           res = await r.json()
           em = discord.Embed(title="Result")
           em.set_image(url=res['message'])
           await interaction.followup.send(embed=em)
        except:
           await interaction.followup.send(traceback.print_exc())

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invite", description="Invite the bot")
    async def _invite(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=1644971949559&scope=bot", ephemeral=True)

    @app_commands.command(name="idavatar", description="Get avatar by ID")
    @app_commands.describe(id="ID of user to get the avatar")
    async def _idavatar(self, interaction: discord.Interaction, id: int):
      userid = int(id)
      user = await bot.get_user(userid)
      avatar = user.avatar.url
      await interaction.response.send_message(avatar)

    @app_commands.command(name='avatar', description='get someone avatar (avatar copy)')
    @app_commands.describe(avamember="Member")
    async def _avatar(self, interaction: discord.Interaction, avamember: discord.Member = None):
       if avamember is None:
           return await interaction.response.send_message(ctx.author.avatar.url)
       userAvatarUrl = avamember.avatar.url
       await interaction.response.send_message(userAvatarUrl)

    @commands.command(name='say', description='say smth')
    @commands.is_owner()
    async def _speak(self, ctx, *, text):
          message = ctx.message
          if message.reference is not None:
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
     embed = discord.Embed(title="Result", description="Brainfuck Interpreter")
     embed.add_field(name="Translate:", value=f"{brainfuck.evaluate(content)}")
     await interaction.response.send_message(embed=embed)
    @app_commands.command(name="ping", description="Pong! <3")
    async def ping(self, interaction: discord.Interaction):
          await interaction.response.send_message(f"Pong!\nLatency: {round(bot.latency * 1000)}")

    @app_commands.command(name="stats", description="bot stats")
    async def stats(self, interaction: discord.Interaction):
      embed = discord.Embed(title=f"Bot stats of {bot.user}", description="Stats:")
      embed.add_field(name="Platform:", value=f"```css \n {platform.system()} {platform.release()} {platform.machine()} \n ```")
      embed.add_field(name="Timezone", value=f"```css \n {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo} \n```")
      embed.add_field(name="Latency", value=f"```css \n{bot.latency * 1000} \n ```")
      embed.add_field(name="Uptime", value=f"```css \n {str(datetime.timedelta(seconds=int(round(time.time()-startTime))))} \n ```")
      embed.add_field(name="Python Version", value=f"```css \n {sys.version} \n ```")
      embed.add_field(name="Discord.py Version", value=f"```css \n {discord.__version__} \n ```")
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
     search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
     await interaction.followup.send("http://www.youtube.com/watch?v=" + search_results[0])

    @app_commands.command(name="webhookspawn")
    @app_commands.describe(name="Webhook Name")
    @app_commands.checks.has_permissions(manage_webhooks=True)
    async def webhookspawn(self, interaction: discord.Interaction, name: str):
     webhook = await interaction.channel.create_webhook(name=name)
     await interaction.user.send(f"Heres your webhook \n {webhook.url}")
     await interaction.response.send_message(f"Created webhook {name}")
# New Music Player, DisMusic Has been deprecated for this bot, Codename : Bullet
# Moved to music.py
# Why i put them in here?, becuz why not
class Music(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @app_commands.command(name="connect", description="Connect to Your Voice")
  async def join(self, interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.user.voice is None:
      return await interaction.followup.send("You are not connected to a voice channel")
    else:
      channel = interaction.user.voice.channel
      vc: wavelink.Player = channel
      await vc.connect(cls=wavelink.Player)
      await interaction.followup.send(f"Connected to voice channel: '{channel}'")


  @app_commands.command(name="playsc", description="Play SoundCloud (Powered by WaveLink)")
  @app_commands.describe(search="Search for song")
  async def playsc(self, interaction: discord.Interaction, search: str):
   if not interaction.guild.voice_client:
    await interaction.user.voice.channel.connect(cls=wavelink.Player)
    vc: wavelink.Player = interaction.guild.voice_client
   else:
    vc: wavelink.Player = interaction.guild.voice_client
   await interaction.response.defer()
   track = await wavelink.SoundCloudTrack.search(query=search, return_first=False)
   dropdig = MusicDropDown(track)
   dropdig.vc = vc
   viewdig = MusicSelectView(timeout=30)
   viewdig.track = track
   await interaction.followup.send(view=MusicSelectView(timeout=30))
   dropdig.message = await interaction.original_response()
   
  @commands.hybrid_command(name="play", description="Play a music from Youtube (Powered by WaveLink)")
  @app_commands.describe(search="Youtube search or URL")
  async def play(self, ctx, *, search: wavelink.YouTubeTrack):
    await ctx.defer()
    if not ctx.voice_client:
      vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"Hey, {ctx.message.author.mention}You are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
    
  @commands.hybrid_command(name="pause", description="Pause song")
  async def pause(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send(f"Music paused by {ctx.message.author.mention}")


  @commands.hybrid_command(name="resume", description="Resume playing")
  async def resume(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send(f"Music is back! by {ctx.message.author.mention}")


  @commands.hybrid_command(name="stop", description="Stop Player")
  async def stop(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send(f"{ctx.message.author.mention} stopped the music.")
  @commands.hybrid_command(name="cleareffect", description="Clear any effect")
  async def effclean(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
      await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.flat()))
      message = await ctx.send("Clearing")
      await asyncio.sleep(5)
      await message.edit(content="Cleared The Filter")

  @commands.hybrid_command(name="bassboost", description="Bass boost goes brr")
  async def bassboost(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
      await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.boost()))
      message = await ctx.send("Applying...")
      await asyncio.sleep(5)
      await message.edit(content="Applied")

  @commands.hybrid_command(name="nightcore", description="Apply NightCore") 
  async def nightcore(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

      await vc.set_filter(wavelink.Filter(timescale=wavelink.Timescale(speed=1.05, pitch=1.2, rate=1.0)))
      await ctx.send("Applied Nightcore (Require 5 sec)")


  @commands.hybrid_command(name="disconnect", description="Disconnect the Bot from VC")
  async def disconnect(self, ctx):
    if not ctx.voice_client:
        return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    await ctx.send(f"{ctx.message.author.mention} send me out :(")


  @commands.hybrid_command(name="loop", description="Loops the song")
  async def loop(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    try:
      vc.loop ^= True
    except Exception:
      setattr(vc, "loop", False)

    if vc.loop:
        embed = discord.Embed(title=" ", description="I will now repeat the current track :repeat_one:")
        return await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=" ", description="I will no longer repeat the current track")
        return await ctx.send(embed=embed)


  @commands.hybrid_command(name="queue", description="Show Queues")
  async def queue(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, im not connected to a voice channel")   
    elif not ctx.author.voice:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty:
      return await ctx.send("Queue is empty!")

    em = discord.Embed(color=0x1A2382, title="Queue")
    copy = vc.queue.copy()
    count = 0
    for song in copy:
      count += 1
      em.add_field(name=f"Position {count}", value=f"`{song.title}`")

    return await ctx.send(embed=em)


  @commands.hybrid_command(name="volume", description="Volume")
  @app_commands.describe(volume="Must be 1 to 300")
  async def volume(self, ctx, volume: int):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if volume > 300:
      await vc.set_volume(volume=300)
      embed = discord.Embed(title=" ", description=f"Volume has been set to {vc.volume}")
      return await ctx.send(embed=embed)
      
    await vc.set_volume(volume=volume)
    embed = discord.Embed(title=" ", description=f"Volume has been set to {vc.volume}")
    return await ctx.send(embed=embed)


  @commands.hybrid_command(name="nowplaying", description="Show what playing now", aliases=['np'])
  async def playing(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
    
    if not vc.is_playing():
      return await ctx.send("Nothing is playing")

    em = discord.Embed(title=f" ", description=f"Playing \n **[{vc.track}]({vc.track.uri})** \n Artist: {vc.track.author}")
    em.set_author(name="Now Playing♪", icon_url=f"{bot.user.avatar.url}")
    bar = progressBar.splitBar(int(vc.track.length), int(vc.position), size=10)
    em.add_field(name="Position", value=f"{bar[0]}")
    em.add_field(name="ㅤ", value="ㅤ")
    em.add_field(name="ㅤ", value="ㅤ")
    em.add_field(name="Position", value=f"`{datetime.timedelta(seconds=vc.position)}`")
    em.add_field(name="Duration", value=f"`{datetime.timedelta(seconds=vc.track.length)}`") 
    em.add_field(name="ㅤ", value="ㅤ")
    em.add_field(name="ㅤ", value="ㅤ")
    em.set_footer(icon_url=f"{ctx.author.avatar.url}", text=f"Requested by {ctx.author}")
    return await ctx.send(embed=em)



  @commands.hybrid_command(name="skip", description="Skip a song")
  async def skip(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    
    embed = discord.Embed(title=" ", description=f"[{vc.track}]({vc.track.uri}) has been skipped", color=discord.Color.from_rgb(0, 255, 0))
    await ctx.send(embed=embed)
    await vc.stop()


  @commands.hybrid_command(name="qremove", description="Remove amount of queue")
  async def qremove(self, ctx, index: int):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if index > len(vc.queue) or index < 1:
      return await ctx.send(f"Index must be between 1 and {len(vc.queue)}")

    removed = vc.queue.pop(index - 1)

    await ctx.send(f"{ctx.message.author.mention} removed `{removed.title}` from the queue")

  @commands.hybrid_command(name="qclean", description="Clear queue")
  async def qclear(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

      vc.queue.clear()
    return await ctx.send(f"{ctx.message.author.mention} cleared the queue.")
   
  @commands.hybrid_command(name='lyrics', description='Genius Lyrics')
  @app_commands.describe(artist="Artist of song", title="Song")
  async def lyrics(self, ctx, artist, *, title):
     try:
      song = genius.search_song(title, artist)
      lyric = song.lyrics
      print(lyric[:lyric.rfind("Embed")])
      embedgenius = discord.Embed(title=f"{song.title} by {song.artist}", description=f"\n{lyric[:lyric.rfind('Embed')]}")
      await ctx.send(embed=embedgenius)
     except Exception as e:
      await ctx.send(f"Something wrong, Report this to !        from ender import bot#2105\n Logs: \n ```py\n{e}\n```")

token = os.getenv("TOKEN")



async def node_connect(bot):
  await wavelink.NodePool.create_node(bot=bot, host="lavalink.oops.wtf", port=443, password="www.freelavalink.ga", https=True)



bot.run(token)
