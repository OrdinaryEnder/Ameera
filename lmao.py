import brainfuck
import qrcode
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
from mod.botmod import bypass
from mod.botmod import track_end
import youtube_dl
import aiohttp
import asyncio
import time
import datetime
import datetime as dt
import typing as t
from email.base64mime import body_encode
import wavelink

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

with open('badwords.txt', 'r') as f:
    words = f.read()
    badword = words.split()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents)

# Badword Test (haha lol)



@bot.event
async def on_ready():
 print("Logged As")
 print(f"@{bot.user.name}#{bot.user.discriminator}")
 print("Registering Commands (Wont take long time)....")
 print("Adding Music cogs")
 await bot.load_extension('mod.music')
 await node_connect(bot)
 node_ready(bot)
 track_end(bot)
 print("Adding Fun Cogs")
 await bot.add_cog(Fun(bot))
 print("Adding Moderation Cogs")
 await bot.add_cog(Moderation(bot))
 print("Adding Other Cogs")
 await bot.add_cog(Other(bot))
 print("Adding Owner Cogs")
 await bot.add_cog(Owner(bot))
 print("Adding Nsfw Cogs")
 await bot.add_cog(nsfw(bot))
 print("Support us at https://github.com/zairullahdev/Alexandra")

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
       if badwords in (message.content.lower()).split(' '):
            await message.delete()
            await message.channel.send("meow no swer")
            await bot.process_commands(message)
            break
       else:
            print("Checked")
            await bot.process_commands(message)
            return
     
6
@bot.event
async def on_connect():
      await bot.change_presence(activity=discord.Game(name="Testing"))

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
             'I am tired. *proceeds with sleeping*',
             'Dont ask stupid question like that']
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

    @commands.command(name="qrgen", description="Generates QR using Data (Can be URL or Anything")
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
          await ctx.channel.purge(limit=1, check=lambda m: m.author == bot.user)
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
    @commands.command(name="eval", description="Quick Eval (Codeblock)")
    @commands.is_owner()
    async def eval(self, ctx, *, code):
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
    @commands.command(name="timeout", description="had enough?, Mute still annoy u?, Try timeout")
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member: discord.Member, time, *, reason=None):
     time_convert = {"s":1, "m":60, "h":3600, "d":86400}
     tempmute= int(time[:-1]) * time_convert[time[-1]]
     await member.timeout(datetime.timedelta(seconds=tempmute), reason=reason)
     embed = discord.Embed(title="Timed out", description=f"Timed out user: {member.mention}\n \n For {time} \n \n Tryna Leave ur still can get timed out haha", color=0xe74c3c)
     await ctx.send(embed=embed)

    @commands.command(name="untimeout", description="Untimeout user", aliases=["rmtimeout"])
    @commands.has_permissions(kick_members=True)
    async def untimeout(self, ctx, member: discord.Member):
     await member.timeout(None)
     embed = discord.Embed(title="Untimed out", description="Untimed out {member.mention}", color=0x2ecc71)
     await ctx.send(embed=embed)

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
         await ctx.send("Unbanned")
    @commands.command(name="idban", description="Ban using ID (For Unfair Leaver")
    @commands.has_permissions(ban_members=True)
    async def _idban(self, ctx, id, reason=None):
        user = await bot.fetch_user(int(id))
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"Banned @{user.name}#{user.discriminator}, Reason = {reason}")

    @commands.command(name='mute', description='Mute Whos Keep Spamming on ur Holy Server')
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
         mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

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
    @commands.command(name='image', description='Get Images (NSFW!!!!!)\n Current Possible:\n hass, hmidriff, pgif, 4k, hentai, holo, hneko, neko, hkitsune, kemonomimi, anal, hanal, gonewild, kanna, ass, pussy, thigh, hthigh, gah, coffee, food, paizuri, tentacle, boobs, hboobs, yaoi')
    @commands.is_nsfw()
    async def _image(self, ctx, image):
     img = image
     r = requests.get(f"https://nekobot.xyz/api/image?type={image}")
     res = r.json()
     em = discord.Embed()
     em.set_image(url=res['message'])
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
          return

    @commands.command(name='brainfuck', description='Yet another BrainFuck Interpreter In Discord')
    async def _brainfuck(self, ctx, *, code):
     content = re.sub("```brainfuck|```bf|```", "", code)
     embed = discord.Embed(title="Result", description="Brainfuck Interpreter")
     embed.add_field(name="Translate:", value=f"{brainfuck.evaluate(content)}")
     await ctx.send(embed=embed)

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
          await ctx.send(f"Pong!\nLatency: {round(bot.latency * 1000)}")

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
# New Music Player, DisMusic Has been deprecated for this bot, Codename : Bullet
# Moved to music.py
# Why i put them in here?, becuz why not

async def node_connect(bot):
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot, host='lava.link', port=80, password='alexandra', https=False)

def node_ready(bot):
  @bot.event
  async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")


token = os.getenv("TOKEN")


bot.run(token)
