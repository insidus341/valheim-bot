FROM python:3.9.2-buster

RUN apt-get update && apt install python3-pip -y

COPY app /app

WORKDIR /app

RUN pip3 install -r requirements.txt 

CMD ["bot.py"]

ENTRYPOINT ["python3"]