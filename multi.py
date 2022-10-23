from discord import Interaction
from discord import app_commands
from discord.ext import commands
import discord
import asyncio

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
tree = bot.tree


@bot.event
async def on_ready():
    await bot.tree.sync()


@tree.command()
async def monsoon(interaction: discord.Interaction):
    await interaction.response.defer()
    await asyncio.sleep(3)
    await interaction.followup.send("Good Morning USA!")
    await asyncio.sleep(3)
    await interaction.followup.send("I got a feeling that it's gonna be a wonderful day!")
    await asyncio.sleep(3)
    await interaction.followup.send("The sun in sky has a smile on his face and it's shining a salute to the American Race")
    await asyncio.sleep(5)
    await interaction.followup.send("Oh boy! it's swell to say")
    await asyncio.sleep(2)
    await interaction.followup.send("Good Morning USA!")


bot.run("OTk0NDI2OTYzOTQ5MjY1MDA3.GE5ixx.LB-UPwra5_qQIqFxq9g2kvtQN69H9OxZRYbUF0")
