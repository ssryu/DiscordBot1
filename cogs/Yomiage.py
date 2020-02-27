import asyncio
import logging
import datetime
import os
import queue
import hashlib
import re

import discord
from discord.ext import tasks, commands

from google.auth import compute_engine
from google.cloud import texttospeech

from db.session import session
from db.replace_word import ReplaceWord

logger = logging.getLogger(__name__)


class Yomiage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.yomiage_channel_name = None
        self.play_queue = queue.Queue()

    @tasks.loop(seconds=1.0)
    async def retry_play(self):
        # 再生キューが空なら何もしない
        if self.play_queue.empty():
            return

        # VC入ってなければ何もしない
        if self.vc is None:
            return

        filename, is_after_remove = self.play_queue.get()
        logger.debug(filename)
        logger.debug(is_after_remove)

        try:
            if self.vc.is_playing():
                # 再生中の場合は何もせずキューに戻す
                self.play_queue.put((filename, is_after_remove))
            else:
                self.vc.play(discord.FFmpegPCMAudio(filename),
                             after=lambda err: self.my_after(err, filename, is_after_remove))
        except discord.ClientException as e:
            logger.info('retry...')
            logger.info(e)
            # 再度キューに乗せ直す
            self.play_queue.put((filename, is_after_remove))

        self.play_queue.task_done()

    def play_voice(self, filename, is_after_remove=False):
        t = (filename, is_after_remove)
        self.play_queue.put(t)

    @commands.command(name='タチコマァ！ついてこい！')
    async def join_voice_chat(self, ctx):
        """ VCにタチコマを呼び出す """

        # VCに接続していなければ接続する
        if self.vc is None:
            channel = ctx.author.voice.channel
            self.vc = await channel.connect(timeout=2.0, reconnect=True)

            # 挨拶メッセージを読み上げる
            self.play_voice('join_voice.m4a')

            # 読み上げを行うチャンネルを確定させる
            self.yomiage_channel_name = ctx.channel.name

            self.retry_play.start()
            await ctx.channel.send('はーい！')

    @commands.command(name='ばいばい')
    async def leave_voice_chat(self, ctx):
        """ VCからタチコマを切断させる """
        if self.vc is None:
            # VoiceChannelに未接続の場合はメッセージを返すだけ
            await ctx.channel.send('VCに繋いでないよっ！')
            return

        # VoiceChannelに接続している場合は接続を切断し、メッセージを返す
        await self.vc.disconnect()

        self.vc = None
        self.yomiage_channel_name = None
        self.retry_play.stop()  # キューの消化を止める
        self.clear_play_queue()  # キューの中身をクリアする

        await ctx.channel.send('またねっ！')

    def clear_play_queue(self):
        # 再生待ちを全てクリアする
        while not self.play_queue.empty():
            filename, is_after_remove = self.play_queue.get()
            self.my_after(None, filename, is_after_remove)

        self.play_queue.task_done()

    @commands.command(name='シッ！')
    async def stop_voice(self, ctx):
        """ 読み上げを中断させる """
        self.vc.stop()
        self.clear_play_queue()

    @commands.command(name='辞書登録')
    async def add_dictionary(self, ctx, keyword, replace_word):
        """ 辞書登録 {語句} {読み方} """
        a = ReplaceWord.add(session, keyword, replace_word)
        await ctx.channel.send(f'{keyword} の読みを {replace_word} で登録しました〜！')

    @commands.command(name='辞書')
    async def list_dictionary(self, ctx):
        """ 登録されている読み替え辞書をすべて表示する """
        words = ReplaceWord.all(session)
        a = [f'{x.id}: {x.keyword}, {x.replace_to}' for x in words]
        msg = "```\n"
        msg += '\n'.join(a)
        msg += "```"
        await ctx.channel.send(msg)

    @commands.command(name='辞書削除')
    async def delete_dictionary(self, ctx, id):
        """ 辞書削除 {id} """
        words = ReplaceWord.delete(session, id)
        await ctx.channel.send(f'ID: {words.id}, keyword: {words.keyword}, replace_to: {words.replace_to} を削除しました〜！')

    @staticmethod
    def my_after(error, file, is_after_remove=False):
        # is_after_removeがTrueの時だけ削除を行う
        if is_after_remove:
            logger.debug(f'delete temp voice file: {error} {file}')
            os.remove(file)

    @staticmethod
    def create_voice(ssml):
        """ Google Cloud Text-to-Speech を利用してssmlから音声ファイルを生成する """
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml)

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ja-JP',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        return client.synthesize_speech(synthesis_input, voice, audio_config)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """ 新しい人がVCに接続してきたらいらっしゃいメッセージを読み上げる """
        # logger.debug(member.name)
        # logger.debug(before)
        # logger.debug(after)
        if member == self.bot.user:
            return

        if before is None:
            logger.info("before is None")
            return

        if after is None:
            logger.info("after is None")
            return

        if after.channel is not None:
            if self.vc is not None:
                if self.vc.channel.name != after.channel.name:
                    logger.debug(after.channel)
                    logger.debug(self.vc.channel.name)
                    logger.info("yomiage_channel_name not equal after.channel.name")
                    return

                if before.self_mute != after.self_mute:
                    # ミュート切り替えには反応しないようにする
                    logger.info("self_mute changed.")
                    return

                member_name = self.convert_replace_dictionary(member.name)
                input_text = f'<speak>{member_name}さん やっほー！</speak>'

                voice = self.create_voice(input_text)

                tmp_filename = f'{datetime.datetime.now().timestamp()}.mp3'

                with open(tmp_filename, 'wb') as out:
                    out.write(voice.audio_content)
                    self.play_voice(tmp_filename, True)

    @staticmethod
    def convert_replace_dictionary(input_text):
        replace_dictionary = ReplaceWord.all(session)

        for x in replace_dictionary:
            input_text = input_text.replace(x.keyword, x.replace_to)

        return input_text

    @staticmethod
    def replace_url(input_text):
        regex = re.compile(r"http\S+")
        return re.sub(regex, 'URL', input_text)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # 自分自身の発言で反応しないように絶対必須
        if ctx.author == self.bot.user:
            return

        # VCに繋がっていないなら読み上げ処理する必要ないので
        if self.vc is None:
            return

        # 読み上げ中のチャンネル以外の発言も流れ込んでくるので、それは読み上げない
        if self.yomiage_channel_name != ctx.channel.name:
            return

        name = self.convert_replace_dictionary(ctx.author.name)
        content = self.convert_replace_dictionary(ctx.content)
        content = self.replace_url(content)

        input_text = f'<speak>{name}<break time="300ms"/>{content}</speak>'
        logger.debug(input_text)

        response = self.create_voice(input_text)

        byte_timestamp = str(datetime.datetime.now().timestamp()).encode()
        filename = hashlib.md5(byte_timestamp).hexdigest()
        suffix = '.mp3'
        tmp_filename = filename + suffix
        logger.debug(tmp_filename)

        with open(tmp_filename, 'wb') as out:
            out.write(response.audio_content)
            logger.debug(f'Audio content written to file "{tmp_filename}"')
            self.play_voice(tmp_filename, True)


def setup(bot):
    bot.add_cog(Yomiage(bot))
