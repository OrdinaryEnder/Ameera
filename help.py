from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def help(ctx):
 embed=discord.Embed(title="Alexandra Bot", url="https://discord.com/api/oauth2/authori>
 embed.set_author(name="ZairullahDeveloper", url="https//github.com/zairullahdev", icon>
 embed.set_thumbnail(url="https://camo.githubusercontent.com/51f16d28861eade2210bb6c541>
 embed.add_field(name="Play", value="Play a music from YouTube ", inline=True)
 embed.add_field(name="Stop", value="Stop music", inline=True)
 embed.add_field(name="Leave ", value="Leave music voice", inline=True)
 embed.add_field(name="kick", value="Kick A Member", inline=True)
 embed.add_field(name="ban", value="Ban a member", inline=True)
 embed.add_field(name="mute", value="Mute a member", inline=True)
 embed.add_field(name="unmute ", value="Unmute them", inline=True)
 embed.add_field(name="lvbyass ", value="Bypass Linkvertise", inline=True)
 embed.add_field(name="print", value="Print Current Session, Queue")
 embed.set_footer(text="Report or suggest something at https://github com/zairullahdev/>
 await ctx.send(embed=embed)
