FROM python:3.8.0-alpine3.10

WORKDIR /usr/src/app

ENV MULTIDICT_NO_EXTENSIONS=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "/usr/src/app/run_bot.py" ]
