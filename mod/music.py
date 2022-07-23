# Music Module
import datetime
import random
from lyricsgenius import Genius
import discord
import wavelink
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

genius = Genius()

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="play", description="Play a music from Youtube (Powered by WaveLink)")
  async def play(self, ctx, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
      vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"Hey, {ctx.message.author.mention}You are not connected to a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if vc.queue.is_empty and not vc.is_playing():
      await vc.play(search)
      embed = discord.Embed(title="Now playing", description=f"{search.title}\n \n Artist: {search.author}")
      embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
      await ctx.send(embed=embed)
    else:
      await vc.queue.put_wait(search)
      await ctx.send(f"Added {search.title} to the queue")
    vc.ctx = ctx
    setattr(vc, "loop", False)


  @commands.command(name="pause", description="Pause song")
  async def pause(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.pause()
    await ctx.send(f"Music paused by {ctx.message.author.mention}")


  @commands.command(name="resume", description="Resume playing")
  async def resume(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.resume()
    await ctx.send(f"Music is back! by {ctx.message.author.mention}")


  @commands.command(name="stop", description="Stop Player")
  async def stop(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    await ctx.send(f"{ctx.message.author.mention} stopped the music.")


  @commands.command(name="disconnect", description="Disconnect the Bot from VC")
  async def disconnect(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.disconnect()
    await ctx.send(f"{ctx.message.author.mention} send me out :(")


  @commands.command(name="loop", description="Loops the song")
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
      return await ctx.send("Loop is now Enabled!")
    else:
      return await ctx.send("Loop is now Disabled!")


  @commands.command(name="queue", description="Show Queues")
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


  @commands.command(name="volume", description="Volume")
  async def volume(self, ctx, volume: int):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    if volume > 100:
      return await ctx.send("Thats to high...")
    elif volume < 0:
      return await ctx.send("Thats to low...")

    await ctx.send(f"Set the volume to {volume}%")
    return await vc.set_volume(volume=volume)


  @commands.command(name="nowplaying", description="Show what playing now", aliases=['np'])
  async def playing(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client
    
    if not vc.is_playing():
      return await ctx.send("Nothing is playing")

    em = discord.Embed(title=f"Now playing {vc.track}", description=f"Artist: {vc.track.author}")
    em.add_field(name="Duration", value=f"`{datetime.timedelta(seconds=vc.track.length)}`")
    em.add_field(name="Extra info", value=f"Song URL: [Click Me]({str(vc.track.uri)})")
    return await ctx.send(embed=em)



  @commands.command(name="skip", description="Skip a song")
  async def skip(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.stop()
    return await ctx.send(f"{ctx.message.author.mention} skipped the actual music.")


  @commands.command(name="remove", description="Remove amount of queue")
  async def remove(self, ctx, index: int):
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

  @commands.command(name="qclean", description="Clear queue")
  async def qclear(self, ctx):
    if not ctx.voice_client:
      return await ctx.send(f"Hey {ctx.message.author.mention}, you are not connected to a voice channel")   
    elif not getattr(ctx.author.voice, "channel", None):
      return await ctx.send(f"{ctx.message.author.mention} first you need to join a voice channel")
    else:
      vc: wavelink.Player = ctx.voice_client

    await vc.queue.clear()
    return await ctx.send(f"{ctx.message.author.mention} cleared the queue.")
   
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

async def setup(bot):
  await bot.add_cog(Music(bot))

