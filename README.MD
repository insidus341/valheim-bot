# Project Title

Valheim server bot for Discord

## What does it do?

The Discord bot listens to the following messages:

`!status` - returns "Server is Online/Offline"

`!players` - returns "There are ### players connected"

`!join` - returns "You can join the server by copying this IP 0.0.0.0 and pasting (ctrl + v) in game. Password is mysecretpass."

`!mods` - only active if `VALHEIM_PLUS` = 1 - provides instructions on how to install Valheim plus on a client

`!help` - shows this menu


## Getting Started

These instructions will get you the Valheim server bot running on your Valheim server.

### Prerequisites

```
Docker
Git
A dedicated Valheim server
A Discord bot
```

### Installing

A Valheim dedicated server is needed. You can use one of these projects to bring a server online:

https://github.com/lloesche/valheim-server-docker

https://github.com/mbround18/valheim-docker


You need to create Discord bot with `Send Messages` and `Read Message History` permissions. Full instructions can be found here: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

The easiest way to install is to clone the Github project, edit docker-compose.yaml and then run `docker-compose up -d`. There are a few required environmentals to include in `docker-compose.yaml`:
```
DISCORD_TOKEN = The Discord token for your Discord bot
SERVER_IP = The IP address of the Valheim server
SERVER_PORT = The Port of the Valheim server (default is 2457)
SERVER_PASSWORD = The password for the Valheim server (leave blank if there is no password)
VALHEIM_PLUS = Change to 0 if Valheim Plus is not installed 
```

## Built With

* [Docker](https://www.docker.com/)
* [Pyhton3](https://www.python.org/download/releases/3.0/)
* [Discord](https://discord.com/)

## Authors

* **James Earl** - [Insidus341](https://github.com/Insidus341)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
