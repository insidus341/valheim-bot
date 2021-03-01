FROM python:3.9.2-alpine3.13

RUN apt install python3-pip --no-cache

COPY app /app

WORKDIR /app

RUN pip3 install -r requirements.txt 

CMD ["bot.py"]

ENTRYPOINT ["python3"]