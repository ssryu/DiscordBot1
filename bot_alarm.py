import asyncio
import bot_messages   as bm
import bot_properties as bp
from datetime import datetime

agenda = []

def reserve(message):
    try:
        content = message.content.split(" ")
        if len(content) == 4:
            minute = int(content[1])
            second = int(content[2])
            agenda.append((minute, second, content[3]))
            return "予約に成功しました。"
        else:
            return "予約に失敗しました。ヘルプを参照してください。"
    except:
        return "予約に失敗しました。ヘルプを参照してください。"

def get_list():
    msg = "```\n"
    for i, a in enumerate(agenda, 1):
        msg += "{0:2d}) {1:02d}:{2:02d} > {3}\n".format(i, a[0], a[1], a[2])
    msg += "```"
    return msg

def delete_reserve(message):
    try:
        content = message.content.split(" ")
        if len(content) == 2:
            index = int(content[1]) - 1
            del agenda[index]
            return "削除に成功しました。"
        else:
            return "削除に失敗しました。ヘルプを参照してください。"
    except:
        return "削除に失敗しました。ヘルプを参照してください。"

async def alarm(client):
    # クライアントが起動するまで待つ
    await client.wait_until_ready()
    # クライアントからチャンネル情報を取得
    alarmchannel = client.get_channel(bp.alarm_channel_id)
    # チャンネル取得できなたっからアラーム機能終了
    if alarmchannel == None:
        return
    # while not client.is_closed:
    while True:
        now = datetime.now()
        d, h, m = (now.weekday(), now.hour, now.minute)
        if h == 21 and m == 25:
            await alarmchannel.send("```ギルド討伐5分前！```")
        elif h == 11 and m == 55:
            msg = "```ワールドボス「" + bm.boss[d][0] + "」出現5分前！```"
            await alarmchannel.send(msg)
        elif h == 19 and m == 55:
            msg = "```ワールドボス「" + bm.boss[d][1] + "」出現5分前！```"
            await alarmchannel.send(msg)

        delete_list = []
        for a in agenda:
            if a[0] == h and a[1] == m:
                await alarmchannel.send(a[2])
                delete_list.append(a)
        for a in delete_list:
            agenda.remove(a)

        await asyncio.sleep(60)
