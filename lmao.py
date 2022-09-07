from StringProgressBar import progressBar
import platform
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

badlist = ["sex", "fuck", "shit", "gay", "luzer sucks", "happylemon suck", "zach suck", "sh^t", "yo mama", "deez nut"]

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

with open('badwords.txt', 'r') as f:
    words = f.read()
    badword = words.split()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='+', intents=intents)
# Badword Test (haha lol)

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

    for badwords in badword:

       if badlist in message.content.lower().split():
            await message.delete()
            webhook = await message.channel.create_webhook(name="dis webhook")
            await webhook.send(username=f"{message.author.name}#{message.author.discriminator}", avatar_url=message.author.avatar, content=f"{ '#' * len(message.content)}")
            await webhook.delete()
            return

       elif message.author.guild.owner.mention in message.content.lower().split(' '):
            await message.author.timeout(datetime.timedelta(seconds=300))
            await message.delete()
            await message.channel.send(f"{message.author.mention} Has Been Timed out for 5 minute \n Reason : pinging owner")
            return
       elif "UwU" in message.content.lower():
           await message.delete()
           embed = discord.Embed(title=f"{message.author} said the forbidden word uwu!", description=" ")
           embed.set_image(url="https://tenor.com/view/i-am-the-storm-that-is-approaching-gif-26009898")
           await message.channel.send(embed=embed)
    await bot.process_commands(message)
    return
     

@bot.event
async def on_connect():
      await bot.change_presence(activity=discord.Game(name="Testing"))
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

bot.help_command = MyHelpCommand()

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
     self.bot = bot
     super().__init__()
 
    @commands.hybrid_command(name='lvbypass', description='Bypass Linkvertise (powered by bypass.vip)')
    @app_commands.describe(url="URL About to Bypass (Example: https://linkvertise.com/38666/ArceusXRoblox")
    async def _lvbypass(self, ctx, url):
       link = await bypass(url)
       loadlink = json.dumps(link)
       finalink = json.loads(loadlink)
       print(finalink)
       datalink = finalink.get("destination")
       embed=discord.Embed(title="Result", description="Dont let your data get sold by Them!")
       embed.add_field(name="ㅤ", value=datalink)
       await ctx.send(embed=embed)


    @commands.hybrid_command(name='8ball', description='Let the 8 Ball Predict!\n')
    @app_commands.describe(question="The question")
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
             'I am tired. *proceeds with sleeping*',
             'Dont ask stupid question like that']
     response = random.choice(responses)
     embed=discord.Embed(title="The Magic 8 Ball has Spoken!")
     embed.add_field(name='Question: ', value=f'{question}', inline=True)
     embed.add_field(name='Answer: ', value=f'{response}', inline=False)
     await ctx.send(embed=embed)


    @commands.hybrid_command(name='akinator', description="Lemme guess ur character")
    async def akinator(self, ctx):
     await ctx.send("Akinator is disabled for sone reason")
     

    @commands.hybrid_command(name="date", description="Show today date (UTC)")
    async def __date(self, ctx):
     date = datetime.datetime.now().strftime("%Y-%m-%d")
     time = datetime.datetime.now().strftime("%H:%M:%S")
     embed=discord.Embed(title="Now", description=f"Today is")
     embed.add_field(name="Date", value=date)
     embed.add_field(name="Time", value=time)
     embed.set_footer(text="If you wanna donate to us your can execute donate command")
     await ctx.send(embed=embed)
       
    @commands.hybrid_command(name="math", description="Math")
    @app_commands.describe(num="Needed number", operation="+ for summation ,- for subtraction , * for multiplication, / for divine", num2="another number")
    async def __math(self, ctx, num: int, operation, num2: int):
     if operation not in ['+', '-', '*', '/']:
         await ctx.send('Please type a valid operation type. (+ for summation ,- for subtraction , * for multiplication, ÷ for divine)')
     var = f'{num} {operation} {num2}'
     embed = discord.Embed(title="Result", description="ㅤ", color=discord.Color.from_rgb(0, 0, 0))
     embed.add_field(name="Result Of Your Math:", value=f"{var} = {eval(var)}")
     embed.set_footer(text="Be Smart Next Time!")
     await ctx.send(embed=embed)

    @commands.hybrid_command(name="meme", description="Reddit Memes")
    async def meme(self, ctx):
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

            await ctx.send(embed=embed)
    @commands.hybrid_command(name="linuxmemes", description="Linux funny memes")
    async def linuxmeme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/linuxmemes/new.json?sort=hot") as r:
                res = await r.json()
                embed=discord.Embed(title="Linux Memes", description=" ")
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    
    @commands.command(name="meow", description="meow", hidden=True)
    async def meow(self, ctx):
     embed = discord.Embed(title="Ender was here", description="He say meow (hi!) to you!")
     embed.set_author(name="Your found ender!", url="https://github.com/OrdinaryEnder", icon_url="https://i.ibb.co/qgFpJzF/Png-1.png")
     await ctx.send(embed=embed)

    @commands.hybrid_command(name="linusquotes", description="Get Better Motivation from Linus Torvalds!")
    async def quotes(self, ctx):
     async with aiohttp.ClientSession() as session:
         async with session.get('https://linusquote.com/quote') as r:
 
          load = await r.json()
          jsonload = json.dumps(load)
          final = json.loads(jsonload)
          print(final['body'])
          embed = discord.Embed(title="Linus Torvalds Once Said:", description="ㅤ")
          embed.add_field(name="ㅤ", value=f"{final['body']}")
          await ctx.send(embed=embed)

    @commands.hybrid_command(name="qrgen", description="Generates QR using Data (Can be URL or Anything")
    @app_commands.describe(data="URL Or String")
    async def qrgen(self, ctx, *, data):
     img = qrcode.make(data)
     img.save("temp.png")
     embed = discord.Embed(title="Successfully Generated", description="Result")
     file = discord.File("temp.png", filename="image.png")
     embed.set_image(url="attachment://image.png")
     await ctx.send(embed=embed, file=file)
     os.remove("temp.png")

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gcclean")
    @commands.is_owner()
    async def gc(self, ctx):
     await ctx.send(f"Cleaned {gc.collect()} Garbage Collections")

    @commands.hybrid_command(name="shutdown", description="Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
     await ctx.send("ALT+F4 PRESSED")

     await ctx.send("Bye :(")
     await bot.close()

    @commands.hybrid_command(name='shell', description='Console Remote')
    @commands.is_owner()
    @app_commands.describe(cmd="The Command About to executed in shell")
    async def _eval(self, ctx, *, cmd):
        # Ender : This very  damger dont give it to your friend ig D:<
        await ctx.send(f"Current Shell = {os.getenv('SHELL')}")
        results = subprocess.check_output(cmd, shell=True)
        lmao = results.decode("utf-8")

        await ctx.send(f"```css\n{ lmao }```")

    @commands.hybrid_command(name='restart', description='Restart Bot Session')
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

    @commands.hybrid_command(name='chpresence', description='Change Bot Presence As You Wanted')
    @commands.is_owner()
    @app_commands.describe(status="Status to be displayed", name="The text", twittch="Twitch URL For Streaming")
    async def _chp(self, ctx, status: typing.Literal['playing', 'watching', 'listening', 'streaming', 'sleep'], *, name, twittch=None):
          await ctx.defer()
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
            
    @commands.hybrid_command(name="eval", description="Quick Eval (Codeblock)")
    @app_commands.describe(code="The code about to executed")
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

    @commands.hybrid_command(name="awaiteval", description="Await an eval")
    @commands.is_owner()
    @app_commands.describe(code="Await Execution")
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

    @commands.hybrid_command(name="timeout", description="had enough?, Mute still annoy u?, Try timeout")
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(member="Valid Member", time="For example, 1d is for 1 day, s for second, m for minutes, h for hour, d for day", reason="The reason")

    async def timeout(self, ctx, member: discord.Member, time, *, reason=None):
     time_convert = {"s":1, "m":60, "h":3600, "d":86400}
     tempmute= int(time[:-1]) * time_convert[time[-1]]
     await member.timeout(datetime.timedelta(seconds=tempmute), reason=reason)
     embed = discord.Embed(title="Timed out", description=f"Timed out user: {member.mention}\n \n For {time} \n \n Tryna Leave ur still can get timed out haha", color=0xe74c3c)
     await ctx.send(embed=embed)

    @commands.hybrid_command(name="untimeout", description="Untimeout user", aliases=["rmtimeout"])
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(member="Timed out member")
    async def untimeout(self, ctx, member: discord.Member):
     await member.timeout(None)
     embed = discord.Embed(title="Untimed out", description=f"Untimed out {member.mention}", color=0x2ecc71)
     await ctx.send(embed=embed)

    @commands.hybrid_command(name='kick', description='Kick Dumbass from Your Holy Server')
    @app_commands.describe(member="Member About to kicked", reason="Reason")
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, reason=None):
                await ctx.guild.kick(Member, reason=reason)
                await ctx.send(f"{Member} Successfully kicked by {ctx.author.mention}")

    @commands.hybrid_command(name='ban', description='Ban dumbass from your Holy Server')
    @app_commands.describe(user="Member About to banned", reason="Reason")
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"Successfully banned {user} by {ctx.author.mention}, reason={reason}")
    @commands.hybrid_command(name='unban', description='Unban people who have repented')
    @app_commands.describe(id="ID of Member About to unban")
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, id):
         user = await bot.fetch_user(int(id))
         await ctx.guild.unban(user)
         await ctx.send(f"Unbanned @{user.name}#{user.discriminator}")
    @commands.command(name="idban", description="Ban using ID (For Unfair Leaver")
    @app_commands.describe(member="ID of Member About to banned", reason="Reason")
    @commands.has_permissions(ban_members=True)
    async def _idban(self, ctx, id, *, reason=None):
        user = await bot.fetch_user(int(id))
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"Banned @{user.name}#{user.discriminator}, Reason = {reason}")

    @commands.hybrid_command(name='mute', description='Mute Whos Keep Spamming on ur Holy Server')
    @app_commands.describe(member="Member to be muted", time="Time (example: 1y", reason="Reason")
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
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True)
                embed = discord.Embed(title="Muted!", description=f"{member.mention} was muted   for {time}, dont leave the server or you'll get banned! ", colour=discord.Colour.light_gray())
                embed.add_field(name="Reason:", value=reason, inline=True)
                await ctx.send(embed=embed)
                await member.add_roles(mutedRole, reason=reason)
                await asyncio.sleep(tempmute)
                await member.send(f"You have been unmuted from {guild.name}, Dont break rules again!")
                await member.remove_roles(mutedRole)
                return



    @commands.hybrid_command(name='unmute', description='Unmute')
    @app_commands.describe(member="Member")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
         mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

         await member.remove_roles(mutedRole)
         await member.send(f" you have unmutedd from: - {ctx.guild.name}")
         embed = discord.Embed(title="Unmuted", description=f" Unmuted {member.mention}")
         await member.add_roles(memberrole)
         await ctx.send(embed=embed)
       
    @commands.hybrid_command(name='purge', description='Purge Old Messages')
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(limit="How much ur gonna delete")
    async def _purge(self, ctx, limit: int):
         await ctx.channel.purge(limit=limit)
         await ctx.send("Purged by {}".format(ctx.author.mention), delete_after=5)
         await ctx.message.delete()

    @commands.hybrid_command(name='nick', description='Change Nickname of people')
    @commands.has_permissions(manage_nicknames=True)
    @app_commands.describe(member="Member", nick="New Nickname")
    async def chnick(self, ctx, member: discord.Member, *, nick):
     await member.edit(nick=nick)
     await ctx.send(f'Nickname was changed for {member.mention} ')


class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="image", description="Get Images (NSFW!!!!!)")
    @commands.is_nsfw()
    @app_commands.describe(image="NSFW Image about to show")
    async def _image(self, ctx, *, image: typing.Literal['hass', 'hmidriff', 'pgif', 'hentai', 'holo', 'hneko', 'neko', 'hkitsune', 'kemonomimi', 'anal', 'hanal', 'gonewild', 'kanna', 'ass', 'pussy', 'thigh', 'hthigh', 'gah', 'coffee', 'food', 'paizuri', 'tentacle', 'boobs', 'hboobs', 'yaoi']):
     try:
         await ctx.defer()
         async with aiohttp.ClientSession() as session:
          async with session.get(f"https://nekobot.xyz/api/image?type={image}") as r:
           res = await r.json()
           em = discord.Embed(title="Result")
           em.set_image(url=res['message'])
           await ctx.send(embed=em)
     except:
        await ctx.send(traceback.print_exc())

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="idavatar", description="Get avatar by ID")
    @app_commands.describe(id="ID of user to get the avatar")
    async def _idavatar(self, ctx, id):
      userid = int(id)
      user = await bot.fetch_user(userid)
      avatar = user.avatar.url
      await ctx.send(avatar)

    @commands.hybrid_command(name='avatar', description='get someone avatar (avatar copy)')
    @app_commands.describe(avamember="Member")
    async def _avatar(self, ctx, avamember : discord.Member):
       userAvatarUrl = avamember.avatar.url
       await ctx.send(userAvatarUrl)

    @commands.hybrid_command(name='say', description='say smth')
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

    @commands.command(name="runpython", description="Run Python Codes")
    async def pycode(self, ctx, *, content):
     code = re.sub("```python|```py|```", "", content)
     async with aiohttp.ClientSession() as session:
      async with session.post("https://linksafe.repl.co/api/eval/", data=code, raise_for_status=True) as response:
           embed = discord.Embed(title="Result", description=f"Here your code result {ctx.author.mention} \n {await response.json()}")
           return await ctx.send(embed=embed)

    @commands.hybrid_command(name='brainfuck', description='Yet another BrainFuck Interpreter In Discord')
    @app_commands.describe(code="brainfuck code")
    async def _brainfuck(self, ctx, *, code):
     content = re.sub("```brainfuck|```bf|```", "", code)
     embed = discord.Embed(title="Result", description="Brainfuck Interpreter")
     embed.add_field(name="Translate:", value=f"{brainfuck.evaluate(content)}")
     await ctx.send(embed=embed)

    @commands.hybrid_command(name='robloxinfo', description='Get Roblox Game Info')
    @app_commands.describe(placeid="Roblox Place ID")
    async def _robloxinfo(self, ctx, *, placeid):
   # First we gonna get Universe ID, Because Roblox Only Allow show game with it
     await ctx.defer()
     async with aiohttp.ClientSession() as session:
         async with session.get(f'https://api.roblox.com/universes/get-universe-containing-place?placeid={placeid}') as uidget:
          universeload = await uidget.json()
          load = json.dumps(universeload)
          getid = json.loads(load)
# and finally, post your universe id into roblox
     async with aiohttp.ClientSession() as session:
         async with session.get(f"https://games.roblox.com/v1/games?universeIds={getid['UniverseId']}") as robloxgame:
          returngame = await robloxgame.json()
          getinfogame = json.dumps(returngame, indent=4, sort_keys=True)
  # send it as json because this is for developer
     jsonroblox = '```'
     await ctx.send(f'```json\n{ getinfogame }\n```')

    @commands.hybrid_command(name='upload', description='Upload Files Into transfer.sh')
    async def upfile(self, ctx):
     bonk = ctx.message.attachments[0]
     url = bonk.url
     local_filename = url.split('/')[-1]
     # NOTE: Changing to aiohttp due to discord.py requirements

     async with aiohttp.ClientSession(raise_for_status=True) as session:
       async with session.get(url) as r:
                f = await aiofiles.open(local_filename, mode='wb') 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                await f.write(await r.read())
                await f.close()
     files = {'file': open(local_filename, 'rb')}
     async with aiohttp.ClientSession() as session:
         async with session.post('https://transfer.sh', data=files) as up:
          print(up.text())
          embed = discord.Embed(title='Result', description=f"{await up.text()}")
          embed.set_footer(text="Powered by https://transfer.sh")
          await ctx.send(embed=embed)
     # Because it already done lets remove it
     os.remove(local_filename)

    @commands.hybrid_command(name="donate", description="Donate using PayPal (Indonesia Only)")
    async def donate(self, ctx):
     embed=discord.Embed(title="Donate", description="")
     embed.set_image(url="https://i.ibb.co/pn6LLZj/Donation.png")
     await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping", description="Pong! <3")
    async def ping(self, ctx):
          await ctx.send(f"Pong!\nLatency: {round(bot.latency * 1000)}")
    @commands.hybrid_command(name="stats", description="bot stats")
    async def stats(self, ctx):
      await ctx.defer()
      embed = discord.Embed(title=f"Bot stats of {bot.user}", description="Stats:")
      embed.add_field(name="Platform:", value=f"```css \n {platform.system()} {platform.release()} {platform.machine()} \n ```")
      embed.add_field(name="Timezone", value=f"```css \n {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo} \n```")
      embed.add_field(name="Latency", value=f"```css \n{bot.latency * 1000} \n ```")
      embed.add_field(name="Uptime", value=f"```css \n {str(datetime.timedelta(seconds=int(round(time.time()-startTime))))} \n ```")
      embed.add_field(name="Python Version", value=f"```css \n {sys.version} \n ```")
      embed.add_field(name="Discord.py Version", value=f"```css \n {discord.__version__} \n ```")
      await ctx.send(embed=embed)

    @commands.hybrid_command(name="search", description="Search Youtube Videos")
    @app_commands.describe(search="Youtube Video To Search")
    async def yt(self, ctx, *, search):
     query_string = urllib.parse.urlencode({
        "search_query": search
     })
     html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
     )
     search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
     await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])

    @commands.hybrid_command(name="webhookspawn")
    @app_commands.describe(name="Webhook Name")
    @commands.has_permissions(manage_webhooks=True)
    async def webhookspawn(self, ctx, *, name):
     webhook = await ctx.channel.create_webhook(name=name)
     await ctx.author.send(f"Heres your webhook \n {webhook.url}")
# New Music Player, DisMusic Has been deprecated for this bot, Codename : Bullet
# Moved to music.py
# Why i put them in here?, becuz why not
class Music(commands.Cog):
  def __init__(self, bot):
   self.bot = bot

  @commands.hybrid_command(name="connect", description="Connect to Your Voice")
  async def join(self, ctx):
    await ctx.defer()
    if ctx.author.voice is None:
      return await ctx.send("You are not connected to a voice channel")
    else:
      channel = ctx.author.voice.channel
      vc: wavelink.Player = channel
      await vc.connect(cls=wavelink.Player)
      await ctx.send(f"Connected to voice channel: '{channel}'")


  @commands.hybrid_command(name="playsc", description="Play SoundCloud (Powered by WaveLink)")
  @app_commands.describe(search="Search for song")
  async def playsc(self, ctx, *, search: str):
    await ctx.defer()
    if not ctx.voice_client:
      vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"Hey, {ctx.message.author.mention}You are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
     
    if vc.queue.is_empty and not vc.is_playing():
      track = await wavelink.SoundCloudTrack.search(query=search)
      await vc.play(track[0])
      embed = discord.Embed(title="Now playing", description=f"[{track[0].title}]({track[0].uri}) \n \n Author: {track[0].author}")
      embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
      await ctx.send(embed=embed)
    else:
      track = await wavelink.SoundCloudTrack.search(query=search)
      await vc.queue.put_wait(track[0])
      await ctx.send(f"Added {search} to the queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)

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

    if vc.queue.is_empty and not vc.is_playing():
      await vc.play(search)
      embed = discord.Embed(title="Now playing", description=f"[{search.title}]({search.uri})\n \n Uploader: {search.author}")
      embed.set_thumbnail(url=search.thumbnail)
      embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
      await ctx.send(embed=embed)
    else:
      await vc.queue.put_wait(search)
      await ctx.send(f"Added {search.title} to the queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)


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
      embed = discord.Embed(title=" ", description=f"Volume has been set to {volume}")

    if volume > 300:
      await vc.set_volume(volume=300)
      return await ctx.send(embed=embed)
      
    await vc.set_volume(volume=volume)
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

async def node_connect(bot):
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot, host="51.161.130.134", port=10436, password="youshallnotpass")


token = os.getenv("TOKEN")


bot.run(token)
