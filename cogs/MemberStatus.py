import logging
import discord
from discord.ext import commands
import googleapiclient.discovery
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class MemberStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='戦闘力')
    async def my_combat_point(self, ctx, *, member: discord.Member = None):
        msg = "```\n"
        msg += '\n'.join(self.get_my_combat_point())
        msg += "```"
        await ctx.channel.send(msg)

    @staticmethod
    def get_credentials():
        client_secret_file = 'client_secret.json'
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]
        credentials = service_account.Credentials.from_service_account_file(client_secret_file, scopes=scopes)
        return credentials

    def get_my_combat_point(self):
        spreadsheet_id = '1HK96UyIEEiX3Q67yMzpA-bc5eLi0jHm3pgJSTXFnqkY'
        range_name = 'メンバー情報一覧!A1:P'

        credentials = self.get_credentials()
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  credentials=credentials,
                                                  cache_discovery=False)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
        values = result.get('values', [])

        logger.info(values)
        return ['てｓｔ']


def setup(bot):
    bot.add_cog(MemberStatus(bot))
