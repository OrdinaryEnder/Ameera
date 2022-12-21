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


async def setup(bot):
    await bot.add_cog(nsfw(bot))
