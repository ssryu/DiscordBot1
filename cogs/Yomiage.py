import asyncio
import logging

import discord
from discord.ext import commands

from google.cloud import texttospeech

logger = logging.getLogger(__name__)


class Yomiage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.yomiage_ch = None

    @commands.command(name='タチコマァ！ついてこい！')
    async def join_voice_chat(self, ctx):
        if self.vc is None:
            channel = ctx.author.voice.channel
            self.vc = await channel.connect()
            self.vc.play(discord.FFmpegPCMAudio('join_voice.m4a'), after=self.my_after)
            self.yomiage_ch = ctx.channel
            await ctx.channel.send('はーい！')

    @commands.command(name='ばいばい')
    async def leave_voice_chat(self, ctx):
        if self.vc is None:
            await ctx.channel.send('VCに繋いでないよっ！')
        else:
            await self.vc.disconnect()
            self.vc = None
            self.yomiage_ch = None
            await ctx.channel.send('またねっ！')

    @staticmethod
    def voice_play_error(ctx, er):
        ctx.channel.send('読み上げエラーが発生しました')

    def my_after(self, error):
        if error:
            coro = self.yomiage_ch.send('Song is done!')
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                # an error happened sending the message
                pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logger.info(member.name)
        logger.info(before)
        logger.info(after)
        if member == self.bot.user:
            return

        if before is None:
            return

        if before.channel is None:
            if after.channel is not None:
                if self.vc is not None:
                    input_text = f'<speak>{member.name}さん やっほー！</speak>'

                    client = texttospeech.TextToSpeechClient()
                    synthesis_input = texttospeech.types.SynthesisInput(ssml=input_text)

                    voice = texttospeech.types.VoiceSelectionParams(
                        language_code='ja-JP',
                        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

                    audio_config = texttospeech.types.AudioConfig(
                        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

                    response = client.synthesize_speech(synthesis_input, voice, audio_config)

                    with open('comming.mp3', 'wb') as out:
                        out.write(response.audio_content)
                        self.vc.play(discord.FFmpegPCMAudio('comming.mp3'), after=self.my_after)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # 自分自身の発言で反応しないように絶対必須
        if ctx.author == self.bot.user:
            return

        input_text = f'<speak>{ctx.author.name}<break time="300ms"/>{ctx.content}</speak>'
        logger.info(input_text)

        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(ssml=input_text)

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ja-JP',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        with open('output.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            logger.info('Audio content written to file "output.mp3"')

            self.vc.play(discord.FFmpegPCMAudio('output.mp3'), after=self.my_after)
        return


def setup(bot):
    bot.add_cog(Yomiage(bot))
