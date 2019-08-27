import asyncio
import discord
import random
from datetime import datetime

import bot_alarm      as ba
import bot_messages   as bm
import bot_properties as bp

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-'*20)

@client.event
async def on_message(message):
    # ヘルプ表示
    if message.content == 'ヘルプ'\
    or message.content == 'へるぷ':
        msg = bm.help_message()
        await message.channel.send(msg)
    # サイコロ1~100
    elif message.content == 'サイコロ'\
    or message.content == 'さいころ':
        msg = bm.dice_message(message)
        await message.channel.send(msg)
    # スロット
    elif message.content == 'スロット'\
    or message.content == 'すろっと':
        msg = bm.slot_message(message)
        await message.channel.send(msg)
    # ボス案内
    elif message.content == 'ボス'\
    or message.content == 'ぼす':
        msg = bm.boss_message()
        await message.channel.send(msg)
    # 予約
    elif message.content.startswith('!予約'):
        try:
            content = message.content.split(" ")
            if len(content) == 4:
                minute = int(content[1])
                second = int(content[2])
                ba.reserve(minute, second, content[3])
                await message.channel.send("予約に成功しました。")
            else:
                await message.channel.send("予約に失敗しました。ヘルプを参照してください。")
        except:
            await message.channel.send("予約に失敗しました。ヘルプを参照してください。")

client.loop.create_task(ba.alarm(client)) 
client.run(bp.bot_token)
