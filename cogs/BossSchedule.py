import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone, timedelta

import discord
from apiclient import discovery
from discord.ext import commands
from google.oauth2 import service_account

import bot_properties as bp

logger = logging.getLogger(__name__)


class BossSchedule(commands.Cog):
    def __init__(self, bot, calendar_id):
        self.bot = bot
        self.calendar_id = calendar_id

    @commands.command(name='ボス')
    async def boss_message(self, ctx, *, member: discord.Member = None):
        msg = "```\n"
        msg += '\n'.join(self.one_week_boss_schedule_messages())
        msg += "```"
        await ctx.channel.send(msg)

    @staticmethod
    def get_credentials():
        scope = [
            'https://www.googleapis.com/auth/calendar'
        ]

        service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
        credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

        return credentials

    def get_schedule(self, calendar_id, time_min, time_max):
        try:
            credentials = self.get_credentials()

            service = discovery.build('calendar', 'v3', credentials=credentials, cache_discovery=False)

            events = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                maxResults=20
            ).execute()
            items = events['items']

            return items

        except Exception as e:
            logger.error(traceback.format_exc(sys.exc_info()[2]))

    def one_week_boss_schedule_messages(self):
        now = datetime.now(timezone.utc).astimezone()

        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = week_start.isoformat('T')

        week_end = now + timedelta(days=(7 - now.weekday()))
        week_end = week_end.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_end.isoformat('T')

        schedules = self.get_schedule(
            self.calendar_id,
            week_start,
            week_end
        )
        before_sort = [(x["summary"], datetime.fromisoformat(x['start']['dateTime']).weekday(), x['start']['dateTime']) for x in schedules]
        sorted_schedules = sorted(before_sort, key=lambda x: datetime.fromisoformat(x[2]))

        weekday = ('月', '火', '水', '木', '金', '土', '日')
        return [v + ' : ' + ' / '.join([x[0] for x in sorted_schedules if x[1] == i]) for i, v in enumerate(weekday)]


def setup(bot):
    bot.add_cog(BossSchedule(bot, bp.boss_calendar_id))
