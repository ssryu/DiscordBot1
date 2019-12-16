FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY client_secret.json .
COPY . .

CMD [ "python", "/usr/src/app/run_bot.py" ]
