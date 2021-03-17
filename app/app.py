import os
from dotenv import load_dotenv
from bot import DiscordBot
from statistics import ServerStatistics
from multiprocessing import Process

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
VALHEIM_PLUS = int(os.getenv('VALHEIM_PLUS'))

INFLUXDB_HOST = os.getenv('INFLUXDB_HOST')
INFLUXDB_PORT = os.getenv('INFLUXDB_PORT')
INFLUXDB_DATABASE = os.getenv('INFLUXDB_DATABASE')

STATISTICS = os.getenv('STATISTICS')

if DISCORD_TOKEN is None or SERVER_IP is None or SERVER_PORT is None:
    exit(1)

def run():
    # pbot = Process(target=start_bot)
    # pss = Process(target=start_statistics)

    # pbot.start()
    # pss.start()
    if STATISTICS is None:
        start_bot()
    elif STATISTICS == "1":
        start_statistics()

def start_bot():
    bot = DiscordBot()
    bot.init(SERVER_ADDRESS, SERVER_DOMAIN, SERVER_PASSWORD, VALHEIM_PLUS)
    bot.run(DISCORD_TOKEN)

def start_statistics():
    statistics = ServerStatistics(SERVER_ADDRESS, SERVER_DOMAIN, INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE)
    statistics.run()


if __name__ == "__main__":
    run()