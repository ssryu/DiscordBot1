import asyncio
import bot_properties as bp
from datetime import datetime

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
            msg = "```ワールドボス「" + bp.boss[d][0] + "」出現5分前！```"
            await alarmchannel.send(msg)
        elif h == 19 and m == 55:
            msg = "```ワールドボス「" + bp.boss[d][1] + "」出現5分前！```"
            await alarmchannel.send(msg)
        await asyncio.sleep(60)