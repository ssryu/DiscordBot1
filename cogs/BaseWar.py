import calendar
import collections
import unicodedata
from datetime import datetime, date, timedelta, timezone, time
import logging
import os
import googleapiclient.discovery
from google.oauth2 import service_account

import discord
import pytz
from discord.ext import commands

from db.map import Map
from db.basewar import BaseWar as BaseWarModel, 参加受付中の拠点戦がない, 参加種別が不正, 参加VC状況が不正, 参加者がいない, メンバーが見つからない
from db.member import Member
from db.basewar_resources import BaseWarResources
from db.session import session

logger = logging.getLogger(__name__)

days = ['日', '月', '火', '水', '木', '金', '土']


class BaseWar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spreadsheet_id = '1HK96UyIEEiX3Q67yMzpA-bc5eLi0jHm3pgJSTXFnqkY'

    @staticmethod
    def get_credentials():
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        credentials = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
        return credentials

    def get_spreadsheet_service(self):
        credentials = self.get_credentials()
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  credentials=credentials,
                                                  cache_discovery=False)
        return service

    @commands.command(name='拠点戦オープン')
    @commands.has_role('攻殻機動隊')
    async def 拠点戦オープン(self, ctx, map_id=None, event_date=None):
        """拠点戦オープン {2020-03-05 形式の日付(default=当日)}"""
        if map_id is None:
            await ctx.channel.send("「拠点戦オープン {map_id}」という形式で指定してください")
            return

        try:
            map_id = int(unicodedata.normalize('NFKC', map_id))
        except ValueError as e:
            await ctx.channel.send("マップIDは数値で指定してください")
            return

        拠点 = Map.マップIDで拠点情報を取得(session, map_id)

        if 拠点 is not None:
            # イベント日付が指定されていなければ当日として扱う
            tz_tokyo = pytz.timezone('Asia/Tokyo')
            if event_date is None:
                event_date_tokyo = tz_tokyo.localize(datetime.now())
            else:
                event_date_tokyo = tz_tokyo.localize(datetime.strptime(event_date, '%Y-%m-%d'))

            BaseWarModel.拠点戦情報を登録する(session, map_id, event_date_tokyo.date())

            マップID = 拠点.マップマスタ_id
            地域名 = 拠点.マップマスタ.地域マスタ_collection[0].地域名
            マップ名 = 拠点.マップマスタ.マップ名
            拠点曜日 = days[拠点.曜日]
            拠点等級 = 拠点.等級
            map_filename = f"{拠点曜日}_{拠点等級}_{マップ名}"

            file = discord.File(f"拠点戦マップ画像/{map_filename}.PNG", filename=f"map.png")
            embed = discord.Embed(
                title=f"拠点戦 参加者受け付け開始 {マップ名}",
                description=f"ID:{マップID} {拠点曜日}曜日 {拠点等級}等級 {地域名}",
                color=discord.Colour.from_rgb(13, 82, 149))
            embed.set_image(url=f"attachment://map.png")
            await ctx.channel.send(file=file, embed=embed)
        else:
            await ctx.channel.send(f"マップID {map_id} が見つかりませんでした")

    @commands.command(name='拠点戦クローズ')
    @commands.has_role('攻殻機動隊')
    async def 拠点戦クローズ(self, ctx, event_date=None):
        """拠点戦クローズ {2020-03-05 形式の日付(default=当日)}"""
        tz_tokyo = pytz.timezone('Asia/Tokyo')

        if event_date is None:
            event_date_tokyo = tz_tokyo.localize(datetime.now())
        else:
            event_date_tokyo = tz_tokyo.localize(datetime.strptime(event_date, '%Y-%m-%d'))

        try:
            BaseWarModel.拠点戦の参加を締め切る(session, event_date_tokyo.date())
        except 参加受付中の拠点戦がない as e:
            await ctx.channel.send(f"{event_date_tokyo.date()} 参加受付中の拠点戦情報はありません")
            return

        await ctx.channel.send(f"{event_date_tokyo.date()} の拠点戦をクローズしました！")
        return

    @commands.command(name='拠点戦')
    @commands.has_role('攻殻機動隊')
    async def 拠点戦参加(self, ctx, 参加ステータス='', VCステータス='', event_date=None):
        """拠点戦 {参加,遅刻,欠席} {VC可,VC不可,聞き専} {拠点戦日(2020-01-01形式 default=当日)}"""

        tz_tokyo = pytz.timezone('Asia/Tokyo')
        if event_date is None:
            event_date_tokyo = tz_tokyo.localize(datetime.now())
        else:
            event_date_tokyo = tz_tokyo.localize(datetime.strptime(event_date, '%Y-%m-%d'))

        拠点戦 = BaseWarModel.拠点戦取得(session, event_date_tokyo.date())

        try:
            BaseWarModel.参加(session, ctx.author.id, event_date_tokyo.date(), 参加ステータス, VCステータス)
            await ctx.channel.send(f"{ctx.author.name} {参加ステータス} {VCステータス} で {self.UTC日付を日本の日付に変換(拠点戦.日付)} {拠点戦.拠点マップ.等級}等級 {拠点戦.拠点マップ.マップマスタ.地域マスタ_collection[0].地域名}/{拠点戦.拠点マップ.マップマスタ.マップ名} に申請完了！")
        except メンバーが見つからない as e:
            await ctx.channel.send("まず「入隊 {家門名} {戦闘力} {職名}」といった形でメンバー登録をお願いします！")
        except 参加受付中の拠点戦がない as e:
            await ctx.channel.send("現在、参加受け付け中の拠点戦がありません")
        except 参加種別が不正 as e:
            await ctx.channel.send("参加種別の指定は [ 参加, 遅刻, 拠点放置, 欠席 ] のいずれかを選択してください")
        except 参加VC状況が不正 as e:
            await ctx.channel.send("VC状況の指定は [ VC可, VC不可, 聞き専 ] のいずれかを選択してください")

    @commands.command(name='出欠確認')
    @commands.has_role('攻殻機動隊')
    async def 拠点戦出欠確認(self, ctx, event_date=None):
        """出欠確認 {拠点戦日(2020-01-01形式 default=当日)}"""
        tz_tokyo = pytz.timezone('Asia/Tokyo')
        if event_date is None:
            event_date_tokyo = tz_tokyo.localize(datetime.now())
        else:
            event_date_tokyo = tz_tokyo.localize(datetime.strptime(event_date, '%Y-%m-%d'))

        拠点戦 = BaseWarModel.拠点戦取得(session, event_date_tokyo.date())

        try:
            参加者一覧 = BaseWarModel.参加者情報取得(session, event_date_tokyo.date())
        except 参加受付中の拠点戦がない as e:
            await ctx.channel.send(f"{event_date_tokyo.date()} 現在、参加受付中の拠点戦がありません")
            return
        except 参加者がいない as e:
            await ctx.channel.send(f"{event_date_tokyo.date()} の拠点戦にはまだ参加申請がありません")
            return

        msg = "```\n"
        msg += f"{self.UTC日付を日本の日付に変換(拠点戦.日付)} {days[拠点戦.拠点マップ.曜日]}曜日\n"
        msg += f"{拠点戦.拠点マップ.等級}等級 {拠点戦.拠点マップ.マップマスタ.地域マスタ_collection[0].地域名}/{拠点戦.拠点マップ.マップマスタ.マップ名}\n"
        msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

        参加人数 = 0
        遅刻人数 = 0
        拠点放置人数 = 0
        欠席人数 = 0
        未回答人数 = 0

        VC可人数 = 0
        VC不可人数 = 0
        聞き専人数 = 0

        参加職 = []

        msg = "```\n"
        msg += "[参加者]:\n"
        for 参加者 in 参加者一覧:
            if 参加者.参加種別マスタ_id == '参加':
                msg += f"\t{参加者.参加VC状況マスタ_id} {参加者.メンバー.メンバー履歴.家門名} {参加者.メンバー.メンバー履歴.職マスタ_職名} {参加者.メンバー.メンバー履歴.戦闘力}\n"
                参加職.append(参加者.メンバー.メンバー履歴.職マスタ_職名)
                参加人数 += 1
        msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

        msg = "```\n"
        msg += "[遅刻者]:\n"
        for 参加者 in 参加者一覧:
            if 参加者.参加種別マスタ_id == '遅刻':
                msg += f"\t{参加者.参加VC状況マスタ_id} {参加者.メンバー.メンバー履歴.家門名} {参加者.メンバー.メンバー履歴.職マスタ_職名} {参加者.メンバー.メンバー履歴.戦闘力}\n"
                参加職.append(参加者.メンバー.メンバー履歴.職マスタ_職名)
                遅刻人数 += 1
        msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

        msg = "```\n"
        msg += "[拠点放置]:\n"
        for 参加者 in 参加者一覧:
            if 参加者.参加種別マスタ_id == '拠点放置':
                msg += f"\t{参加者.参加VC状況マスタ_id} {参加者.メンバー.メンバー履歴.家門名} {参加者.メンバー.メンバー履歴.職マスタ_職名} {参加者.メンバー.メンバー履歴.戦闘力}\n"
                参加職.append(参加者.メンバー.メンバー履歴.職マスタ_職名)
                拠点放置人数 += 1
        msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

        msg = "```\n"
        msg += "[欠席者]:\n"
        for 参加者 in 参加者一覧:
            if 参加者.参加種別マスタ_id == '欠席':
                msg += f"\t{参加者.メンバー.メンバー履歴.家門名} {参加者.メンバー.メンバー履歴.戦闘力} {参加者.メンバー.メンバー履歴.職マスタ_職名}\n"
                欠席人数 += 1
        msg += "\n"
        msg += "```"
        await ctx.channel.send(msg)

        msg = "```\n"
        msg += "[未回答]:\n"
        未回答者 = []
        all_member = Member.在籍中のメンバー全件取得(session)
        member_ids = dict([(member.user_id, member.メンバー履歴.家門名) for member in all_member])
        参加者ID一覧 = [参加者.メンバー_user_id for 参加者 in 参加者一覧]
        for id, name in member_ids.items():
            if id not in 参加者ID一覧:
                未回答者.append(name)
                未回答人数 += 1
        msg += ', '.join(未回答者) + "\n"
        msg += "```"
        await ctx.channel.send(msg)

        msg = "```\n"
        合計申請人数 = 参加人数 + 遅刻人数 + 拠点放置人数 + 欠席人数
        職別参加人数 = collections.Counter(参加職)
        msg += f"参加: {参加人数} 名, 遅刻: {遅刻人数} 名, 拠点放置: {拠点放置人数}, 欠席: {欠席人数} 名\n"
        msg += f"回答合計: {合計申請人数} 名\n"
        msg += f"\n"
        msg += f"未回答: {未回答人数} 名\n"
        msg += "\n"
        for key, val in 職別参加人数.items():
            msg += f"{key}: {val} 名\n"
        msg += "```"

        await ctx.channel.send(msg)

    @commands.command(name='班確認')
    @commands.has_role('攻殻機動隊')
    async def 拠点戦班確認(self, ctx, event_date=None):
        range_name: str = '班ビュー!A:D'
        service = self.get_spreadsheet_service()
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    majorDimension='ROWS',
                                    range=range_name).execute()

        values = result.get('values', [])

        msg = "```\n"

        for row in values:
            班 = row[0]
            家門名 = row[1]
            戦闘力 = row[2]
            職 = row[3]

            msg += f"{班}, {家門名}, {戦闘力}, {職}\n"

        msg += "```\n"

        return await ctx.channel.send(msg)
        # return values[0]


    @staticmethod
    def UTC日付を日本の日付に変換(x):
        tz_tokyo = pytz.timezone('Asia/Tokyo')
        dt_native = datetime.combine(x, time())
        return tz_tokyo.localize(dt_native).date()

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
        if data is not None:
            マップID = data.マップマスタ_id
            地域名 = data.マップマスタ.地域マスタ_collection[0].地域名
            マップ名 = data.マップマスタ.マップ名
            拠点曜日 = days[data.曜日]
            拠点等級 = data.等級
            map_filename = f"{拠点曜日}_{拠点等級}_{マップ名}"

            file = discord.File(f"拠点戦マップ画像/{map_filename}.PNG", filename=f"map.png")
            embed = discord.Embed(
                title=f"{マップ名}",
                description=f"ID:{マップID} {拠点曜日}曜日 {拠点等級}等級 {地域名}",
                color=discord.Colour.from_rgb(13, 82, 149))
            embed.set_image(url=f"attachment://map.png")
            await ctx.channel.send(file=file, embed=embed)
        else:
            await ctx.channel.send("みつかりませんでした！")

    @commands.command(name='資材確認')
    @commands.has_role('攻殻機動隊')
    async def show_base_resource(self, ctx):
        members = Member.在籍中のメンバー全件取得(session)

        msg = "```\n"
        for member in members:
            if len(member.拠点戦資材_collection) <= 0:
                msg += f"{member.メンバー履歴.家門名}  0,  0,  0\n"
            else:
                resources = member.拠点戦資材_collection[0]
                生命の粉 = resources.生命の粉
                頑丈な原木 = resources.頑丈な原木
                黒い水晶の原石 = resources.黒い水晶の原石
                msg += f"{member.メンバー履歴.家門名}  {生命の粉},  {頑丈な原木},  {黒い水晶の原石}\n"
        msg += "```"
        await ctx.channel.send(msg)

        basewar_resources = BaseWarResources.資材集計(session)
        生命の粉 = basewar_resources[0]
        頑丈な原木 = basewar_resources[1]
        黒い水晶の原石 = basewar_resources[2]

        msg = "```\n"
        msg += f"生命の粉: {生命の粉}, 頑丈な原木: {頑丈な原木}, 黒い水晶の原石: {黒い水晶の原石}\n"
        msg += "```"

        await ctx.channel.send(msg)

def setup(bot):
    bot.add_cog(BaseWar(bot))
