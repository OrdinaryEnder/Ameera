import asyncio
import wavelink
import ast
import inspect
import re
import discord
import json
import requests

def bypass(url):

    payload = {
        "url": url,
    }

    r = requests.post("https://api.bypass.vip/", data=payload)
    return r.json()

def track_end(bot):
  @bot.event
  async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
    ctx = player.ctx
    vc: player = ctx.voice_client

    if vc.loop:
      return await vc.play(track)

    try:
      next_song = vc.queue.get()
      await vc.play(next_song)
      embed = discord.Embed(title="Now playing", description=f"{next_song.title}\n \n Uploader: {next_song.author}")
      embed.set_thumbnail(url=next_song.thumbnail)
      embed.set_image(url="https://i.imgur.com/4M7IWwP.gif")
      await ctx.send(embed=embed)
    except wavelink.errors.QueueEmpty:
      await ctx.send("There are no more track")
      await vc.disconnect()
