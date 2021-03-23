# Valheim Server Management with a Discord Bot and Server Statistics stored in InfluxDB

Get the state of your Valheim Server and restart your Valheim server through Discord messages. Store server Statistics in InfluxDB for ingress into Grafana. 

## What does it do?

### Discord Bot

The Discord bot listens and responds to the following messages:

  `!status` - returns "Server is Online/Offline"

  `!players` - returns "There are ### players connected"

  `!join` - returns "You can join the server by copying this IP 0.0.0.0 and pasting (ctrl + v) in game. Password is mysecretpass."

  `!mods` - only active if `VALHEIM_PLUS` = 1 - provides instructions on how to install Valheim plus on a client

  `!help` - shows this menu

Allows specified servers admins to restart the Valheim server with the `!restart_server` command

![Discord Bot Command Output](https://github.com/insidus341/valheim-bot/blob/a1aa377ed698ec6d119730897ddad617e8cfb2a9/documentation/images/discordbot.png)

### Statistics

Stores statistics about your Valheim server, such as the server availability (is it online?) and the player count. * Statistics can only be gathered from public Valheim servers and the statistics are pulled from Steam. 

![Valheim Server Statistics in Grafana](https://github.com/insidus341/valheim-bot/blob/a1aa377ed698ec6d119730897ddad617e8cfb2a9/documentation/images/grafana.png)

## Getting Started

These instructions will get you the Valheim server bot running on your Valheim server.

### Prerequisites

```
Docker
Git
A dedicated Valheim server
A Discord bot
```

## Basic Installation - * Discord bot only *

A Valheim dedicated server is needed. You can use one of these projects to bring a server online:

https://github.com/lloesche/valheim-server-docker

https://github.com/mbround18/valheim-docker


You need to create Discord bot with `Send Messages` and `Read Message History` permissions. Full instructions can be found here: https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

The easiest way to install is to clone the Github project, created the required .bot.env file and then run `docker-compose up -d`. The required environmentals are: 

.bot.env
```
DISCORD_TOKEN= The Discord totken for your Discord bot

SERVER_IP=1.1.1.1 // The IP address of your Valheim server
SERVER_DOMAIN=example.com // The domain name of your Valheim server
SERVER_PORT=2457
SERVER_PASSWORD=superstrongpassword // The Valheim server password
VALHEIM_PLUS=0 // Set to 1 if you're running Valheim Plus
```

If you're only after the Discord bot, delete the `docker-compose.yaml` and rename `docker-compose-bot-only.yaml` to `docker-compose.yaml`

## Full Installation

Complete the basic installation first

### Allowing Discord users to restart the Valheim Server

Admin priviledges are handled by the Discord User ID - you can find your Discord User ID by following this KB: [Where can I find my user/server message ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

Create the file `discord_admin_users.txt` and enter each Discord User ID on their own line. When a command which requires administrator priviliedges is received, such as `!reboot_server`, the User ID of the sender is matched against this file; if a match is found the command is run. 

Once created, the `discord_admin_users.txt` needs to be mapped into the Docker container, this can be done by adding a `Volume` to `valheim-bot` inside `docker-compose.yaml`:
```
volumes:
      - ./discord_admin_users.txt:/app/discord_admin_users.txt
```


In order to controll the Valheim server container, we need also need to map the `docker.sock` into the `valheim-bot` container. 
WARNING: Make sure you understand the risks of involved with mapping `docker.sock` into a container!

To map `docker.sock` into the `valheim-bot` container, create a new volume as follows: 
```
volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

Start the containers with `docker-compose up -d`


Once the above steps are complete you should see the `!restart_server` command in the output from running the `!help` command. If `!reboot_server` is not listed, verify the above steps have been completed. 

### Storing Valheim server statistics to an Influx Database

Two additional .env files need to be created, `.stats.env` and `.influxdb.env`:

.stats.env
```
SERVER_IP=1.1.1.1 // The IP address of your Valheim server
SERVER_DOMAIN=example.com // The domain name of your Valheim server
SERVER_PORT=2457

INFLUXDB_HOST=influxdb // The IP address of the Influxdb host. `172.31.0.3` is written in the `docker-compose` file. This can be changed as required. 
INFLUXDB_DATABASE=valheim-server-statistics // The Influxdb database name
INFLUXDB_PORT=8086 // Default port
```

.influxdb.env
```
INFLUXDB_DATABASE=valheim-server-statistics // The Influxdb database name
INFLUXDB_USERNAME=valheim-server-statistics-user // The Influxdb username
INFLUXDB_PASSWORD=superstrongpassword // The password used to secure the influx database
INFLUXDB_PORT=8086 // Default port
```

Add the relevant parts to `docker-compose.yaml`: 
```
  valheim-statistics: 
    container_name: valheim-server-statistics
    image: insidus341/valheim-server-statistics:latest
    restart: always
    env_file: 
     - .stats.env
    depends_on:
      - "influxdb"
  
  influxdb:
    container_name: valheim-bot-influxdb
    image: docker.io/influxdb:1.8.4
    restart: always
    env_file:
      - .influxdb.env
    volumes:
      - ./data/influxdb:/var/lib/influxdb
    ports:
      - 8086:8086
```

Code for `insidus341/valheim-server-statistics:latest` can be found here: [Github: valheim-statistics](https://github.com/insidus341/valheim-statistics)
Start the containers with `docker-compose up -d`

You should now be able to add the InfluxDB as a datasource within Grafana.

## Built With

* [Docker](https://www.docker.com/)
* [Pyhton3](https://www.python.org/download/releases/3.0/)
* [Discord](https://discord.com/)
* [InfluxDB](https://www.influxdata.com/)

## Authors

* **James Earl** - [Insidus341](https://github.com/Insidus341)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
