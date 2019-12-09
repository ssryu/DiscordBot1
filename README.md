# DiscordBot1
 for black desert guild

# Quickstart

## Docker Compose (Recommended)

`$ cat <<-'EOF' > bot.env
TOKEN=NjQ5MTYzMTE4MjM2NDAxNjg0.Xd4yug.2rA7OnY6H5mSVJW1eAfrsTP_Umk
BOSS_CALENDAR_ID=nv0tktn0occm9lvcb6is10nri8@group.calendar.google.com
GOOGLE_APPLICATION_CREDENTIALS=BDM-WORLDBOSS-CALENDAR.json
EOF`

`$ docker-compose up --build -d bot`

## Python
`$ pip install -r requirements.txt`

`$ export TOKEN=XXXXXXXXXXXXXXXXXXXX`

`$ python run_bot.py`
