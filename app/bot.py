from server_stats import get_server_status, get_players
from pathlib import Path

import os
import discord
import requests_unixsocket
import json

# *********************

CWD = os.getcwd()
DISCORD_ADMIN_USERS = CWD + "/app/discord_admin_users.txt"

# *********************

class DiscordBot(discord.Client):

    DOCKER_CONNECTED = False

    commands = [
        "!help - shows this menu",
        "!join - information on how to join",
        "!status - returns the server status",
        "!players - returns the current player count"
    ]

    discord_admin_users = []

    def init(self, SERVER_ADDRESS, SERVER_DOMAIN, SERVER_PASSWORD, VALHEIM_PLUS, DISCORD_ADMIN_USER):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.SERVER_DOMAIN = SERVER_DOMAIN
        self.SERVER_PASSWORD = SERVER_PASSWORD
        self.VALHEIM_PLUS = VALHEIM_PLUS
        self.DISCORD_ADMIN_USER = DISCORD_ADMIN_USER

        self._valeheim_plus_enabled()
        self._get_discord_admin_users()
        self._check_docker_sock_exists()

    def _valeheim_plus_enabled(self):
        if self.VALHEIM_PLUS == 1:
            self.commands.append("!mods - returns instructions on configuring Valheim Plus")

    def _get_discord_admin_users(self):
        admin_list = Path(DISCORD_ADMIN_USERS)
        
        if admin_list.is_file():
            with open(DISCORD_ADMIN_USERS) as fp:
                lines = fp.readlines()
            
            for line in lines:
                self.discord_admin_users.append(str(line))
    
    def _check_docker_sock_exists(self):
        if self._get_docker_containers():
            self.DOCKER_CONNECTED = True

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        # Make sure we don't action anything if the bot sends a ! command
        if message.author == self.user:
            return

        if '!' in message.content:
            trigger_message = str(message.content).lower()
            trigger_sender = str(message.author.id)

            if trigger_message == '!help' or trigger_message == '!commands':
                print(f"trigger_message: !help")
                msg = ""

                # Append admin messages for admin users only
                if self._is_discord_admin_user(trigger_sender):
                    commands = self.commands

                    if self.DOCKER_CONNECTED:
                        commands.append("!restart_server - restarts the valheim server")
                
                for command in self.commands:
                    msg = msg + command + "\n"
                
                await message.channel.send(msg)

            if trigger_message == '!join':
                print(f"trigger_message: !join")

                msg = self._join()
                await message.channel.send(msg)

            if trigger_message == '!status':
                print(f"trigger_message: !status")

                status = get_server_status(self.SERVER_ADDRESS)
                if status == 1:
                    status = "Online"
                elif status == 0:
                    status = "Offline"

                await message.channel.send(f"Server is {status}")
            
            if trigger_message == '!players':
                print(f"trigger_message: !players")

                try:
                    players = get_players(self.SERVER_ADDRESS)
                    await message.channel.send(f"There are {players} players connected")
                except Exception as e:
                    await message.channel.send(e)  
            
            if trigger_message == '!mods' and self.VALHEIM_PLUS:
                print(f"trigger_message: !mods")

                msg = self._valheim_plus()
                await message.channel.send(msg)
            
            if trigger_message == '!restart_server' and self._is_discord_admin_user(trigger_sender) and self.DOCKER_CONNECTED:
                print(f"trigger_message: !restart_server")

                msg = self._restart_valheim_server()
                await message.channel.send(msg)
        
    def _join(self):
        message = f"You can join the server by copying this domain `{self.SERVER_DOMAIN}` and pasting (ctrl + v) in game. Password is `{self.SERVER_PASSWORD}`."
        if self.VALHEIM_PLUS:
            message = message + " For the best experience, we recommend having Valheim Plus installed. Type `!mods` for instructions on how to install Valheim Plus."
        
        return message

    def _valheim_plus(self):
        message = "Valheim Plus can be installed from here: https://github.com/valheimPlus/ValheimPlus/releases/download/0.9/WindowsClient.zip \n\n"
        # message = message + "Locate your game folder: go into steam and \nRight click the valheim game in your steam library \n\"Go to Manage\" -> \"Browse local files\"\nUnzip the contents of WindowsClient.zip into the Valheim root folder\n\n"
        # message = message + "In the game directory, browse to /BepInEx/config and edit valheim_plus.cfg \nChange `enforceMod=true` to `enforceMod=false`."
        return message 

    def _restart_valheim_server(self):
        msg = ""
        
        containers = self._get_docker_containers()
        if containers is False:
            return

        id = None
        image = None
        
        for container in containers:
            try:
                image = container['Image']

                if image == "lloesche/valheim-server":
                    id = container['Id']
                    break
            except:
                pass

        if id is None or image is None:
            return "unable to restart server"
        
        restart_code = self._send_restart_command()

        if restart_code == 204:
            msg = "The Valheim server has been restarted!"
        else:
            msg = "Unable to restart Valheim server"

        return msg

    def _is_discord_admin_user(self, userid):
        if userid in self.discord_admin_users:
            return True
        else:
            return False

    def _get_docker_containers(self):
        try:
            session = requests_unixsocket.Session()
            containers = session.get('http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/json').json()

            return containers
        
        except:
            print("Unable to connect to /var/run/docker.sock")
            return False
    
    def _send_restart_command(self):
        try:
            session = requests_unixsocket.Session()
            restart = session.post('http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/' + id + '/restart')
            status_code = restart.status_code

            return status_code

        except:
            return False

        

