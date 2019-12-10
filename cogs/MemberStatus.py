import logging
import discord
from discord.ext import commands
import googleapiclient.discovery
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class MemberStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ステータス')
    async def show_my_status(self, ctx, *, member: discord.Member = None):
        msg = "```\n"
        msg += '\n'.join(self.get_my_status(ctx.author.name, ctx.author.discriminator))
        msg += "```"
        await ctx.channel.send(msg)

    @commands.command(name='戦闘力更新')
    async def my_combat_point(self, ctx, cp, *, member: discord.Member = None):
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        user_key = f"{username}#{discriminator}"
        logger.info(user_key)

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

        status = [x for x in values if x[10] == user_key][0]
        logger.info(values.index(status))
        logger.info(values[26])

        member_index = values.index(status)
        update_values = [
            [
                cp
            ]
        ]
        body = {
            'values': update_values
        }
        cp_range_name = f"メンバー情報一覧!I{member_index + 1}"
        result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                        range=cp_range_name,
                                                        valueInputOption='USER_ENTERED',
                                                        body=body).execute()

        msg = f"{username} さんの戦闘力を {cp} に更新しました〜！"
        await ctx.channel.send(msg)

    @staticmethod
    def get_credentials():
        client_secret_file = 'client_secret.json'
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        credentials = service_account.Credentials.from_service_account_file(client_secret_file, scopes=scopes)
        return credentials

    def get_my_status(self, username, discriminator):
        user_key = f"{username}#{discriminator}"
        logger.info(user_key)

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

        status = [x for x in values if x[10] == user_key][0]
        logger.info(status)

        result = [
            f"家門名: {status[1]}",
            f"加入日: {status[2]}",
            f"在籍日数: {status[4]}",
            f"メイン職: {status[7]}",
            f"戦闘力: {status[8]}"
        ]
        return result


def setup(bot):
    bot.add_cog(MemberStatus(bot))
