FROM python:3

WORKDIR /usr/src/app

ENV GOOGLE_CREDENTIALS ""
ENV GOOGLE_APPLICATION_CREDENTIALS google-credentials.json

COPY google-credentials.json .

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .



CMD [ "python", "/usr/src/app/run_bot.py" ]
