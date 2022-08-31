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



