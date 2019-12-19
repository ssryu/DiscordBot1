# DiscordBot1
 for black desert guild

# Quickstart

## Docker Compose (Recommended)

`$ cat <<-'EOF' > bot.env`

`TOKEN=<< DISCORD BOT TOKEN >>`

`BOSS_CALENDAR_ID=nv0tktn0occm9lvcb6is10nri8@group.calendar.google.com`

`GOOGLE_APPLICATION_CREDENTIALS=client_secret.json`

`EOF`

`$ docker-compose up --build -d bot`

## Python

`$ brew install postgresql`

`$ pip install -r requirements.txt`

`$ export TOKEN=<< DISCORD BOT TOKEN >>`

`$ export BOSS_CALENDAR_ID=nv0tktn0occm9lvcb6is10nri8@group.calendar.google.com`

`$ export GOOGLE_APPLICATION_CREDENTIALS=client_secret.json`

`$ python run_bot.py`
