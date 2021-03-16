from server_stats import get_server_status, get_players
from influxdb import InfluxDBClient
import json
import datetime
import time
import socket

class ServerStatistics():

    influx_client = None

    def __init__(self, SERVER_ADDRESS, SERVER_DOMAIN, INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.SERVER_DOMAIN = SERVER_DOMAIN

        self.INFLUXDB_HOST = INFLUXDB_HOST
        self.INFLUXDB_PORT = INFLUXDB_PORT
        self.INFLUXDB_DATABASE = INFLUXDB_DATABASE
        self.INFLUXDB_HOSTNAME = socket.gethostname()

    def start_influx(self):
        self.influx_client = InfluxDBClient(host=self.INFLUXDB_HOST, port=self.INFLUXDB_PORT)
        database_list = self.influx_client.get_list_database()

        self._influxdb_exists(database_list, self.INFLUXDB_DATABASE)

        if self._influxdb_exists(database_list, self.INFLUXDB_DATABASE) is False:
            self.influx_client.create_database(self.INFLUXDB_DATABASE)

        self.influx_client.switch_database(self.INFLUXDB_DATABASE)


    def run(self):
        self.start_influx()

        while True:
            server_status = int(get_server_status(self.SERVER_ADDRESS))
            server_players = int(get_players(self.SERVER_ADDRESS))
            timestamp = datetime.datetime.now().isoformat()

            if server_status is not None and server_players is not None:
                self._insert_data(server_status, server_players, timestamp)

            print(f"Server status: {server_status} - Player count: {server_players}")
            time.sleep(5)

    def _insert_data(self, server_status, server_players, timestamp):
        data = [
            {
                "measurement": "valheim-server-statistics",
                "tags": {
                    "host": self.INFLUXDB_HOSTNAME,
                },
                "time": datetime.datetime.now().isoformat(),
                "fields": {
                    "server_status": server_status,
                    "player_count": server_players
                }
            }
        ]

        self.influx_client.write_points(data)

    def _influxdb_exists(self, database, search):
        for db in database:
            if db['name'] == search:
                return True
        
        return False
