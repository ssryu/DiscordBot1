import random

from discord.ext import commands


class Gurupon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ぐるぽん')
    async def ぐるぽん(self, ctx, *args):
        select = random.randint(0, len(args) - 1)
        await ctx.send(f'選ばれたのは {args[select]} でした！')

def setup(bot):
    bot.add_cog(Gurupon(bot))
