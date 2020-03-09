import logging

from discord.ext import commands

from db.session import session
from db.job_master import JobMaster

logger = logging.getLogger(__name__)


class JobMasterController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='職マスタ')
    async def 職マスタ(self, ctx):
        jobs = JobMaster.全件取得(session)

        msg = "```\n"
        msg += '\n'.join([job.職名 for job in jobs])
        msg += "```"

        await ctx.channel.send(msg)
        return

    @commands.command(name='職マスタ追加')
    async def 追加(self, ctx, job_name):
        JobMaster.追加(session, job_name)
        return

    @commands.command(name='職マスタ削除')
    async def 削除(self, ctx, job_name):
        JobMaster.削除(session, job_name)
        return

def setup(bot):
    bot.add_cog(JobMasterController(bot))
