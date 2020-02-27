import json
import logging
import os
import uuid

import discord
import googleapiclient.discovery
from discord.ext import commands
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class MemberStatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.spreadsheet_id = '1HK96UyIEEiX3Q67yMzpA-bc5eLi0jHm3pgJSTXFnqkY'

    @commands.command(name='ステータス')
    async def show_my_status(self, ctx, *, member: discord.Member = None):
        msg = "```\n"
        msg += '\n'.join(self.get_my_status(ctx.author.name, ctx.author.discriminator))
        msg += "```"
        await ctx.channel.send(msg)

    def get_job_list(self):
        range_name = '職名リスト(新規職が追加されたら編集)!A:A'
        service = self.get_spreadsheet_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    majorDimension='COLUMNS',
                                    range=range_name).execute()
        values = result.get('values', [])
        return values[0]

    @commands.command(name='職変更')
    async def update_job(self, ctx, job_name):
        """職変更 アークメイジ"""
        job_list = self.get_job_list()

        if job_name not in job_list:
            await ctx.channel.send(f'{job_name} という職はしらないなぁ！')
            return

        search_key = self.create_search_key(ctx.author.name, ctx.author.discriminator)

        values = self.get_member_list()
        status = [x for x in values if x[10] == search_key][0]

        member_index = values.index(status)
        update_values = [
            [
                job_name
            ]
        ]
        body = {
            'values': update_values
        }
        cp_range_name = f"メンバー情報一覧!H{member_index + 1}"
        service = self.get_spreadsheet_service()
        result = service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                        range=cp_range_name,
                                                        valueInputOption='USER_ENTERED',
                                                        body=body).execute()
        logging.info(result)
        msg = f"{ctx.author.name} さんの職業を {job_name} に更新しました〜！"
        await ctx.channel.send(msg)

    def get_spreadsheet_service(self):
        credentials = self.get_credentials()
        service = googleapiclient.discovery.build('sheets', 'v4',
                                                  credentials=credentials,
                                                  cache_discovery=False)
        return service

    def get_member_list(self):
        range_name = 'メンバー情報一覧!A1:P'

        service = self.get_spreadsheet_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=range_name).execute()
        values = result.get('values', [])
        return values

    def create_search_key(self, name, discriminator):
        return f"{name}#{discriminator}"

    @commands.command(name='家門登録')
    async def signup_member(self, ctx, 家門名, *, member: discord.Member = None):
        ctx.author.id, 家門名, uuid.uuid4()

    @commands.command(name='キャラクター登録')
    async def signup_character(self, ctx, 職名, *, member: discord.Member = None):
        ctx.author.id, 家門名, uuid.uuid4()

    @commands.command(name='戦闘力更新')
    async def my_combat_point(self, ctx, cp, *, member: discord.Member = None):
        user_key = self.create_search_key(ctx.author.name, ctx.author.discriminator)
        logger.info(user_key)

        values = self.get_member_list()
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
        service = self.get_spreadsheet_service()
        result = service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                        range=cp_range_name,
                                                        valueInputOption='USER_ENTERED',
                                                        body=body).execute()

        msg = f"{ctx.author.name} さんの戦闘力を {cp} に更新しました〜！"
        await ctx.channel.send(msg)

    @staticmethod
    def get_credentials():
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        credentials = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
        return credentials

    def get_my_status(self, username, discriminator):
        user_key = f"{username}#{discriminator}"
        logger.info(user_key)

        values = self.get_member_list()

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
