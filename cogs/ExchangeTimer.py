import discord
import random
import pytz
from datetime import datetime, timedelta
from discord.ext import tasks, commands

from db.exchange_std import ExchangeStandard, 基準時刻が見つからない
from db.session import session
from collections import deque

class ExchangeTimer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.item_list = deque([])

    @tasks.loop(seconds=1.0)
    async def チェック(self, ctx):
        try:
            std_time = ExchangeStandard.最新の取引所基準時刻を取得(session)
        except 基準時刻が見つからない as e:
            return await ctx.send(f'基準時刻の設定がありません')

        tokyo = pytz.timezone('Asia/Tokyo')
        now_dt = datetime.now(tz=pytz.utc).astimezone(tokyo)

        now_hour_std_dt = datetime(now_dt.year, now_dt.month, now_dt.day, now_dt.hour, std_time.minute, std_time.second, 0)
        now_hour_std_dt = tokyo.localize(now_hour_std_dt)

        # 基準時刻の分が、現在時刻の分よりも大きい場合、1時間前から探索開始とする
        if std_time.minute > now_dt.minute:
            delta = timedelta(days=0, seconds=0, microseconds=0,
                              milliseconds=0, minutes=0, hours=1, weeks=0)
            now_hour_std_dt = now_hour_std_dt - delta

        # 取引所の周期が3分周期なので
        next_delta = timedelta(days=0, seconds=0, microseconds=0,
                               milliseconds=0, minutes=3, hours=0, weeks=0)

        is_match = False
        check_dt = None
        while not is_match:
            # チェック中のdatetimeがない場合は基準時刻に加算し,
            # チェック中のdtがあればcheck_dtにどんどん加算していく
            if check_dt is None:
                check_dt = now_hour_std_dt + next_delta
            else:
                check_dt = check_dt + next_delta

            # 加算後のdtが現在時刻を過ぎていたら 1個前のが現時点から最も直近の入札開始時刻
            if check_dt >= now_dt:
                check_dt = check_dt - next_delta
                is_match = True

        next_open_dt = check_dt + next_delta
        next_next_open_dt = next_open_dt + next_delta

        ten_sec_delta = timedelta(days=0, seconds=10, microseconds=0,
                                  milliseconds=0, minutes=0, hours=0, weeks=0)

        now = now_dt.replace(microsecond=0)
        for item in list(self.item_list):
            before_three_min = item['reg_dt'] - next_delta
            after_three_min = item['reg_dt'] + next_delta

            if before_three_min < item['reg_dt'] < after_three_min:
                next_open_dt = next_open_dt - ten_sec_delta
                if next_open_dt == now:
                    # ここで消す
                    item = self.item_list.popleft()
                    await ctx.send(f'{item["name"]} 出品10秒前〜')

                    # 監視対象が空っぽになったら
                    if self.item_list == []:
                        self.チェック.stop()

        # 10秒前だったら告知を出して終わる
        # await ctx.send(f'{registration_dt}: {item_name}')

    async def 次の出品時間を発言(self, ctx):
        try:
            std_time = ExchangeStandard.最新の取引所基準時刻を取得(session)
        except 基準時刻が見つからない as e:
            return await ctx.send(f'基準時刻の設定がありません')

        tokyo = pytz.timezone('Asia/Tokyo')
        now_dt = datetime.now(tz=pytz.utc).astimezone(tokyo)

        now_hour_std_dt = datetime(now_dt.year, now_dt.month, now_dt.day, now_dt.hour, std_time.minute, std_time.second, 0)
        now_hour_std_dt = tokyo.localize(now_hour_std_dt)

        # 基準時刻の分が、現在時刻の分よりも大きい場合、1時間前から探索開始とする
        if std_time.minute > now_dt.minute:
            delta = timedelta(days=0, seconds=0, microseconds=0,
                              milliseconds=0, minutes=0, hours=1, weeks=0)
            now_hour_std_dt = now_hour_std_dt - delta

        # 取引所の周期が3分周期なので
        next_delta = timedelta(days=0, seconds=0, microseconds=0,
                               milliseconds=0, minutes=3, hours=0, weeks=0)

        is_match = False
        check_dt = None
        while not is_match:
            # チェック中のdatetimeがない場合は基準時刻に加算し,
            # チェック中のdtがあればcheck_dtにどんどん加算していく
            if check_dt is None:
                check_dt = now_hour_std_dt + next_delta
            else:
                check_dt = check_dt + next_delta

            # 加算後のdtが現在時刻を過ぎていたら 1個前のが現時点から最も直近の入札開始時刻
            if check_dt >= now_dt:
                check_dt = check_dt - next_delta
                is_match = True

        next_open_dt = check_dt + next_delta
        next_next_open_dt = next_open_dt + next_delta

        ten_sec_delta = timedelta(days=0, seconds=10, microseconds=0,
                                  milliseconds=0, minutes=0, hours=0, weeks=0)

        now_before = now_dt.replace(microsecond=0)
        next_open_dt_str = datetime.strftime(next_open_dt, '%H:%M:%S')
        next_next_open_dt_str = datetime.strftime(next_next_open_dt, '%H:%M:%S')

        msg = "```\n"
        msg += f"現在の取引所基準時刻は {std_time} です\n"
        msg += f"[出品時刻]\n"
        msg += f"次: {next_open_dt_str}\n"
        msg += f"次の次: {next_open_dt_str}\n"
        msg += "```"
        await ctx.send(msg)

    @commands.command(name='基準時刻')
    async def 基準時刻(self, ctx, minute, second):
        tokyo = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz=pytz.utc).astimezone(tokyo)

        std_dt = datetime(now.year, now.month, now.day, now.hour, int(minute), int(second))

        # 分が現時刻の分よりも未来だったら一時間前のものとして扱う
        if(int(minute) > now.minute):
            one_hour_delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
            std_dt = std_dt - one_hour_delta

        ExchangeStandard.更新(session, std_dt)
        await ctx.send(f'取引所の基準時刻を {std_dt} に更新しました！')

    @commands.command(name='取引所登録')
    async def 取引所登録(self, ctx, item_name, minutes):
        try:
            std_time = ExchangeStandard.最新の取引所基準時刻を取得(session)
        except 基準時刻が見つからない as e:
            return await ctx.send(f'基準時刻の設定がありません')

        tokyo = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz=pytz.utc).astimezone(tokyo)

        registration_dt = datetime(now.year, now.month, now.day, now.hour, int(minutes), 0)
        registration_dt = tokyo.localize(registration_dt)

        # 分が現時刻の分よりも未来だったら一時間前のものとして扱う
        if(int(minutes) > now.minute):
            one_hour_delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
            registration_dt = registration_dt - one_hour_delta

        registration_dt_str = datetime.strftime(registration_dt, '%H:%M:%S')

        self.item_list.append({'name': item_name, 'reg_dt': registration_dt})

        # アイテムを登録してチェックループが回ってなければ開始する
        self.チェック.start(ctx)

        await ctx.send(f'{item_name} (取引所登録 {registration_dt_str})')
        return await self.次の出品時間を発言(ctx)

def setup(bot):
    bot.add_cog(ExchangeTimer(bot))
