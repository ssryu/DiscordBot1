import random

boss = [
    ['クザカ', 'カランダ'],
    ['カランダ', 'ヌーベル、激怒したレッドノーズ'],
    ['ヌーベル', 'クザカ、激怒したレッドノーズ'],
    ['クザカ', 'カランダ'],
    ['カランダ', 'ヌーベル'],
    ['クザカ', 'ヌーベル、激怒したレッドノーズ'],
    ['カランダ', 'ヌーベル'],
]
weekday = ['月', '火', '水', '木', '金', '土', '日']

def help_message():
    msg = "```\n"
    msg += "※ひらがなにも対応しています\n"
    msg += "サイコロ : 1~100のランダム数字を出します。\n"
    msg += "スロット : スロットをします。\n"
    msg += "ボス : ボスの出現表を表示します。\n"
    msg += "!予約 : 予約リストを呼びます。\n"
    msg += "!予約 {時} {分} {内容} : アラームを予約します。\n"
    msg += "!予約削除 {番号} : 予約を削除します。\n"
    msg += "```"
    return msg

def dice_message(message):
    randomcase = random.randint(1, 2)
    dice = random.randint(1, 100)
    if randomcase == 1:
        msg = "```" + message.author.name + "さんのサイコロ結果 : " + str(dice) + "```"
    elif randomcase == 2:
        msg = "```" + message.author.name + "さんがサイコロを振りました！ : " + str(dice) + "```"
    return msg

def slot_message(message):
    slot_list = ['1', '2', '3', '4', '5', '6', '7']
    slot1 = random.sample(slot_list, 3)
    slot2 = random.sample(slot_list, 3)
    slot3 = random.sample(slot_list, 3)

    msg = "```" + message.author.name + "さんが回しました！\n"
    msg += "┃  " + slot1[0] + "  ┃  " + slot2[0] + "  ┃  " + slot3[0] + "  ┃\n"
    msg += "┃  " + slot1[1] + "  ┃  " + slot2[1] + "  ┃  " + slot3[1] + "  ┃\n"
    msg += "┃  " + slot1[2] + "  ┃  " + slot2[2] + "  ┃  " + slot3[2] + "  ┃\n"
    msg += "```"
    return msg

def boss_message():
    msg ="```\n"
    for i in range(0, 7):
        msg += weekday[i] + " : " + boss[i][0] + " / " + boss[i][1] + "\n"
    msg += "```"
    return msg