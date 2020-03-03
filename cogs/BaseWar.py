import calendar
import logging

import discord
from discord.ext import commands

from db.map import Map
from db.session import session

logger = logging.getLogger(__name__)


class BaseWar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name='マップ参照')
    # async def showMap(self, ctx):
    #     file = discord.File(f"拠点戦マップ画像/日_1_トレント街角.PNG", filename=f"test.png")
    #     embed = discord.Embed(
    #         title=f"トレント街角",
    #         color=discord.Colour.from_rgb(13, 82, 149))
    #     embed.add_field(name="等級", value=f"1")
    #     embed.add_field(name="曜日", value=f"日曜日")
    #     embed.set_image(url=f"attachment://test.png")
    #     await ctx.channel.send(file=file, embed=embed)

    @staticmethod
    def 拠点マップか(x):
        return bool(len(x.拠点マップ_collection))

    @staticmethod
    def 拠点等級変換(x):
        if BaseWar.拠点マップか(x):
            return x.拠点マップ_collection[0].等級
        else:
            return 'なし'

    @commands.command(name='マップ検索')
    async def searchMap(self, ctx, q):
        """マップ検索 {マップID または マップ名の一部}"""
        data = Map.マップidまたはマップ名で検索(session, q)
        if len(data) > 0:
            msg = "```\n"
            msg += '\n'.join([f"ID: {x.id}, 等級: {BaseWar.拠点等級変換(x)}, 地域名: {x.地域マスタ_collection[0].地域名}, マップ名: {x.マップ名}" for x in data])
            msg += "```"
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("みつかりませんでした！")

    @commands.command(name='拠点マップ')
    async def showBaseMap(self, ctx, id):
        """拠点マップ {マップID}"""
        data = Map.マップIDで拠点情報を取得(session, id)
        if len(data) > 0:
            days = ['日', '月', '火', '水', '木', '金', '土']
            マップID = data.id
            マップ名 = data.マップ名
            拠点曜日 = days[data.拠点マップ_collection[0].曜日]
            拠点等級 = data.拠点マップ_collection[0].等級
            map_filename = f"{拠点曜日}_{拠点等級}_{マップ名}"

            file = discord.File(f"拠点戦マップ画像/{map_filename}.PNG", filename=f"map.png")
            embed = discord.Embed(
                title=f"{マップ名}",
                color=discord.Colour.from_rgb(13, 82, 149))
            embed.add_field(name="ID", value=f"{マップID}")
            embed.add_field(name="等級", value=f"{拠点等級}")
            embed.add_field(name="曜日", value=f"{拠点曜日}")
            embed.set_image(url=f"attachment://map.png")
            await ctx.channel.send(file=file, embed=embed)
        else:
            await ctx.channel.send("みつかりませんでした！")

def setup(bot):
    bot.add_cog(BaseWar(bot))
