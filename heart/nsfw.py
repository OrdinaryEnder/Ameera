from discord import app_commands
from discord.app_commands import AppCommandError
from discord import Interaction
import discord
from discord.ext import commands
from discord.ext import tasks
import json
import aiohttp
import typing




class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="image", description="Get Images (NSFW!!!!!)", nsfw=True)
    @app_commands.describe(image="NSFW Image about to show")
    async def _image(self, interaction: discord.Interaction, image: typing.Literal['4k', 'hentai', 'holo', 'neko', 'ass', 'boobs', 'hentai', 'lesbian', 'gasm',  'lewd', 'pussy', 'cum', 'blowjob', 'feet', 'spank', 'anal']):
            await interaction.response.defer()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.nekos.fun:8080/api/{image}") as r:
                    res = await r.json()
                    em = discord.Embed(title="Result")
                    em.set_image(url=res['image'])
                    await interaction.followup.send(embed=em)


async def setup(bot):
    await bot.add_cog(nsfw(bot))
