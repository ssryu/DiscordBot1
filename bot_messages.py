import asyncio
import random

boss = [
    ['クザカ', 'カランダ'],
    ['カランダ', 'ヌーベル、激怒したレッドノーズ'],
    ['ヌーベル', 'クザカ'],
    ['クザカ', 'カランダ'],
    ['カランダ', 'ヌーベル'],
    ['ヌーベル', 'クザカ、激怒したギアス'],
    ['カランダ', 'ヌーベル'],
]
weekday = ['月', '火', '水', '木', '金', '土', '日']

def help_message():
    msg = "```\n"
    msg += "※ひらがなにも対応しています\n"
    msg += "サイコロ : 1~100のランダム数字を出します。\n"
    msg += "スロット {回数 max : 10} : スロットをします。回数指定なしの場合1回\n"
    msg += "ボス : ボスの出現表を表示します。\n"
    msg += "!予約 : 予約リストを呼びます。\n"
    msg += "!予約 {時} {分} {内容} : アラームを予約します。\n"
    msg += "!予約削除 {番号} : 予約を削除します。\n"
    msg += "```"
    return msg

async def dice_message(message):
    randomcase = random.randint(1, 3)
    dice = random.randint(1, 100)
    if randomcase == 1:
        msg = "```" + message.author.name + "さんのサイコロ結果 : " + str(dice) + "```"
    elif randomcase == 2:
        msg = "```" + message.author.name + "さんがサイコロを振りました！ : " + str(dice) + "```"
    elif randomcase == 3:
        msg = "```" + message.author.name + "さんが出したサイコロの目は！ : " + str(dice) + "```"
    await message.channel.send(msg)

async def slot_message(message):
    # 回数指定
    repeat = 1
    try:
        content = message.content.split(" ")
        if len(content) == 2:
            repeat = int(content[1])
            if repeat > 10:
                repeat = 10
        elif len(content) ==1:
            pass
        else:
            return
    except:
        return

    # スロット
    slot_list = [':cherries:', ':bell:', ':rofl:', ':cat:', ':frog:', ':gem:', ':slot_machine:']
    count = 0
    msg = ""
    for i in range(1, repeat+1):
        slot1 = random.sample(slot_list, 3)
        slot2 = random.sample(slot_list, 3)
        slot3 = random.sample(slot_list, 3)

        msg += "{0}回目：".format(i)

        randomcase = random.randint(1, 3)
        if randomcase == 1:
            msg += message.author.name + "さんが回しました！\n"
        elif randomcase == 2:
            msg += message.author.name + "の渾身のスロット！\n"
        elif randomcase == 3:
            msg += message.author.name + "選手！回しましたッ\n"

        msg += "┃  " + slot1[0] + "  ┃  " + slot2[0] + "  ┃  " + slot3[0] + "  ┃\n"
        msg += "┃  " + slot1[1] + "  ┃  " + slot2[1] + "  ┃  " + slot3[1] + "  ┃\n"
        msg += "┃  " + slot1[2] + "  ┃  " + slot2[2] + "  ┃  " + slot3[2] + "  ┃\n"

        # 揃ったかチェック
        if slot1[0] == slot2[0] == slot3[0]\
        or slot1[1] == slot2[1] == slot3[1]\
        or slot1[2] == slot2[2] == slot3[2]\
        or slot1[0] == slot2[1] == slot3[2]\
        or slot1[2] == slot2[1] == slot3[0]:
            count += 1

    msg += "揃った回数 : {0} / {1}".format(count, repeat)
    await message.channel.send(msg)

def boss_message():
    msg ="```\n"
    for i in range(0, 7):
        msg += weekday[i] + " : " + boss[i][0] + " / " + boss[i][1] + "\n"
    msg += "```"
    return msg
