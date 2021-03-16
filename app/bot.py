import os
import discord
from server_stats import get_server_status, get_players

class DiscordBot(discord.Client):

    commands = [
        "!help - shows this menu",
        "!join - information on how to join",
        "!status - returns the server status",
        "!players - returns the current player count"
    ]

    def init(self, SERVER_ADDRESS, SERVER_DOMAIN, SERVER_PASSWORD, VALHEIM_PLUS):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.SERVER_DOMAIN = SERVER_DOMAIN
        self.SERVER_PASSWORD = SERVER_PASSWORD
        self.VALHEIM_PLUS = VALHEIM_PLUS

        self._valeheim_plus_enabled()

    def _valeheim_plus_enabled(self):
        if self.VALHEIM_PLUS == 1:
            self.commands.append("!mods - returns instructions on configuring Valheim Plus")
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if '!' in message.content:
            if message.content == '!help' or message.content == '!commands':
                print("Help")
                msg = ""
                
                for command in self.commands:
                    msg = msg + command + "\n"
                
                await message.channel.send(msg)

            if message.content == '!join':
                print("join")
                msg = self._join()
                await message.channel.send(msg)

            if message.content == '!status':
                status = get_server_status(self.SERVER_ADDRESS)
                if status == 1:
                    status = "Online"
                elif status == 0:
                    status = "Offline"

                await message.channel.send(f"Server is {status}")
            
            if message.content == '!players':
                print("players")
                try:
                    players = get_players(self.SERVER_ADDRESS)
                    await message.channel.send(f"There are {players} players connected")
                except Exception as e:
                    await message.channel.send(e)  
            
            if message.content == '!mods' and self.VALHEIM_PLUS:
                print("mods")
                msg = self._valheim_plus()
                await message.channel.send(msg)
        
    def _join(self):
        message = f"You can join the server by copying this domain `{self.SERVER_DOMAIN}` and pasting (ctrl + v) in game. Password is `{self.SERVER_PASSWORD}`."
        if self.VALHEIM_PLUS:
            message = message + " For the best experience, we recommend having Valheim Plus installed. Type `!mods` for instructions on how to install Valheim Plus."
        
        return message

    def _valheim_plus(self):
        message = "Valheim Plus can be installed from here: https://github.com/valheimPlus/ValheimPlus/releases/download/0.9/WindowsClient.zip \n\n"
        message = message + "Locate your game folder: go into steam and \nRight click the valheim game in your steam library \n\"Go to Manage\" -> \"Browse local files\"\nUnzip the contents of WindowsClient.zip into the Valheim root folder\n\n"
        message = message + "In the game directory, browse to /BepInEx/config and edit valheim_plus.cfg \nChange `enforceMod=true` to `enforceMod=false`."
        return message 
