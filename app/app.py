import os
from bot import DiscordBot

from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ADMIN_USER = os.getenv('DISCORD_ADMIN_USER')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
VALHEIM_PLUS = int(os.getenv('VALHEIM_PLUS'))

if DISCORD_TOKEN is None or SERVER_IP is None or SERVER_PORT is None:
    exit(1)

def run():
    start_bot()

def start_bot():
    bot = DiscordBot()
    bot.init(SERVER_ADDRESS, SERVER_DOMAIN, SERVER_PASSWORD, VALHEIM_PLUS, DISCORD_ADMIN_USER)
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run()