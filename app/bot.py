import os
import discord
from server_stats import get_server_status, get_players

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')
VALHEIM_PLUS = int(os.getenv('VALHEIM_PLUS'))

if DISCORD_TOKEN is None or SERVER_IP is None or SERVER_PORT is None:
    exit(1)

SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

commands = [
    "!help - shows this menu",
    "!join - information on how to join",
    "!status - returns the server status",
    "!players - returns the current player count"
]

if VALHEIM_PLUS == 1:
    commands.append("!mods - returns instructions on configuring Valheim Plus")

print(commands)

client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!' in message.content:
        if message.content == '!help' or message.content == '!commands':
            print("Help")
            msg = ""
            
            for command in commands:
                msg = msg + command + "\n"
            
            await message.channel.send(msg)

        if message.content == '!join':
            print("join")
            msg = join()
            await message.channel.send(msg)

        if message.content == '!status':
            status = get_server_status(SERVER_IP, SERVER_PORT)
            await message.channel.send(f"Server is {status}")
        
        if message.content == '!players':
            print("players")
            try:
                players = get_players(SERVER_ADDRESS)
                await message.channel.send(f"There are {players} players connected")
            except Exception as e:
                await message.channel.send(e)  
        
        if message.content == '!mods' and VALHEIM_PLUS:
            print("mods")
            msg = valheim_plus()
            await message.channel.send(msg)

def join():
    message = f"You can join the server by copying this IP `{SERVER_IP}` and pasting (ctrl + v) in game. Password is `{SERVER_PASSWORD}`."
    if VALHEIM_PLUS:
        message = message + " For the best experience, we recommend having Valheim Plus installed. Type `!mods` for instructions on how to install Valheim Plus."
    
    return message

def valheim_plus():
    message = "Valheim Plus can be installed from here: https://github.com/valheimPlus/ValheimPlus/releases/download/0.9/WindowsClient.zip \n\n"
    message = message + "Locate your game folder: go into steam and \nRight click the valheim game in your steam library \n\"Go to Manage\" -> \"Browse local files\"\nUnzip the contents of WindowsClient.zip into the Valheim root folder\n\n"
    message = message + "In the game directory, browse to /BepInEx/config and edit valheim_plus.cfg \nChange `enforceMod=true` to `enforceMod=false`."
    return message          

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)