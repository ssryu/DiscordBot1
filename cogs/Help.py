from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        msg = "```\n"
        msg += "※ひらがなにも対応しています\n"
        msg += "サイコロ : 1~100のランダム数字を出します。\n"
        msg += "スロット {回数 max : 10} : スロットをします。回数指定なしの場合1回\n"
        msg += "ボス : ボスの出現表を表示します。\n"
        msg += "戦力 : 自分の登録戦闘力を表示します。\n"
        msg += "!予約 : 予約リストを呼びます。\n"
        msg += "!予約 {時} {分} {内容} : アラームを予約します。\n"
        msg += "!予約削除 {番号} : 予約を削除します。\n"
        msg += "```"
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Help(bot))
