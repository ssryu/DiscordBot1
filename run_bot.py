import logging
import os

from discord.ext import commands

import bot_properties as bp

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(relativeCreated)07d[ms] : %(name)s : %(message)s"))
logger.addHandler(handler)

app_credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
logger.info(app_credentials_path)

bot = commands.Bot(command_prefix='')
bot.load_extension('cogs.Help')
bot.load_extension('cogs.DiceGame')
bot.load_extension('cogs.SlotGame')
bot.load_extension('cogs.BossSchedule')
bot.load_extension('cogs.MemberStatus')
bot.load_extension('cogs.Yomiage')
bot.run(bp.bot_token)

#
# @client.event
# async def on_ready():
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('-' * 20)
#
#
# @client.event
# async def on_message(message):
#     # ヘルプ表示
#     if message.content == 'ヘルプ' \
#         or message.content == 'へるぷ':
#         msg = bm.help_message()
#         await message.channel.send(msg)
#     # サイコロ1~100
#     elif message.content.startswith('サイコロ') \
#         or message.content.startswith('さいころ'):
#         await bm.dice_message(message)
#     # スロット
#     elif message.content.startswith('スロット') \
#         or message.content.startswith('すろっと'):
#         await bm.slot_message(message)
#     # ボス案内
#     elif message.content == 'ボス' \
#         or message.content == 'ぼす':
#         msg = bm.boss_message()
#         await message.channel.send(msg)
#     elif message.content == '戦力' \
#         or message.content == 'せんりょく':
#         msg = bm.my_combat_point()
#         await message.channel.send(msg)
#     # 予約
#     elif message.content == '!予約':
#         msg = ba.get_list()
#         await message.channel.send(msg)
#     elif message.content.startswith('!予約削除'):
#         msg = ba.delete_reserve(message)
#         await message.channel.send(msg)
#     elif message.content.startswith('!予約'):
#         msg = ba.reserve(message)
#         await message.channel.send(msg)
#
# client.loop.create_task(ba.alarm(client))
# client.run(bp.bot_token)
