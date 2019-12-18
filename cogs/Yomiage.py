import asyncio
import logging
import datetime
import os
import queue

import discord
from discord.ext import tasks, commands

from google.auth import compute_engine
from google.cloud import texttospeech

logger = logging.getLogger(__name__)


class Yomiage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.yomiage_ch = None
        self.play_queue = queue.Queue()
        self.retry_play.start()

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
                self.vc.play(discord.FFmpegPCMAudio(filename), after=lambda err: self.my_after(err, filename, is_after_remove))
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
        """ VoiceChannelにボットを呼び出す """

        # VCに接続していなければ接続する
        if self.vc is None:
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()

            # 挨拶メッセージを読み上げる
            self.play_voice('join_voice.m4a')

            self.yomiage_ch = ctx.channel
            await ctx.channel.send('はーい！')
            return

    @commands.command(name='ばいばい')
    async def leave_voice_chat(self, ctx):
        """ VoiceChannelからボットを退去させる """
        if self.vc is None:
            # VoiceChannelに未接続の場合はメッセージを返すだけ
            await ctx.channel.send('VCに繋いでないよっ！')
            return

        # VoiceChannelに接続している場合は接続を切断し、メッセージを返す
        await self.vc.disconnect()
        self.vc = None
        self.yomiage_ch = None
        await ctx.channel.send('またねっ！')

    @commands.command(name='辞書登録')
    async def add_dictionary(self, ctx, keyword, replace_word):
        """ 辞書登録 {語句} {読み方} """
        pass

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
        logger.debug(member.name)
        logger.debug(before)
        logger.debug(after)
        if member == self.bot.user:
            return

        if before is None:
            return

        if before.channel is None:
            if after.channel is not None:
                if self.vc is not None:
                    input_text = f'<speak>{member.name}さん やっほー！</speak>'

                    voice = self.create_voice(input_text)

                    tmp_filename = f'{datetime.datetime.now().timestamp()}.mp3'

                    with open(tmp_filename, 'wb') as out:
                        out.write(voice.audio_content)
                        self.play_voice(tmp_filename, True)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # 自分自身の発言で反応しないように絶対必須
        if ctx.author == self.bot.user:
            return

        # VCに繋がっていないなら読み上げ処理する必要ないので
        if self.vc is None:
            return

        input_text = f'<speak>{ctx.author.name}<break time="300ms"/>{ctx.content}</speak>'
        logger.debug(input_text)

        response = self.create_voice(input_text)

        tmp_filename = f'{datetime.datetime.now().timestamp()}.mp3'
        logger.debug(tmp_filename)

        with open(tmp_filename, 'wb') as out:
            out.write(response.audio_content)
            logger.debug(f'Audio content written to file "{tmp_filename}"')
            self.play_voice(tmp_filename, True)


def setup(bot):
    bot.add_cog(Yomiage(bot))
