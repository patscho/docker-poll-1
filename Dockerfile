FROM python:3

WORKDIR /usr/src/app

ADD flask-poll-master .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./poll.py" ]

