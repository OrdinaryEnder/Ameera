import asyncio
import wavelink
import ast
import inspect
import re
import discord
import json
import requests
import aiohttp

async def bypass(url):

    payload = {
        "url": url,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.bypass.vip/", data=payload) as r:
            return await r.json()

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
      embed = discord.Embed(title=" ", description=f"Start Playing **[{next_song.title}]({next_song.uri})**")
      await ctx.send(embed=embed)
    except wavelink.errors.QueueEmpty:
      await ctx.send("There are no more track")
      await vc.disconnect()
