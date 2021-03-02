import valve.source.a2s
import requests
import json
import os

# https://python-valve.readthedocs.io/en/latest/source.html

# with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
#     info = server.info()
#     server_name = info['server_name']
#     player_count = info['player_count']
    
#     players = server.players()
#     players_online = players['players']
    

def get_server_status(SERVER_IP, SERVER_PORT):
    url = f"http://api.steampowered.com/ISteamApps/GetServersAtAddress/v0001?addr={SERVER_IP}:{SERVER_PORT}&format=json"
    response = requests.get(url)
    data = response.json()['response']
    json.dumps(data, indent=2)

    success = data['success']
    servers = data['servers']

    if success is False:
        return "Unknown"

    if len(servers) >= 1:
        for server in servers:
            if server['gamedir'] == 'valheim':
                return "Online"
        
        return "Offline"
    else:
        return "Offline"

    print(response)
    # with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    #     info = server.info()
    #     server_name = info['server_name']
    #     player_count = info['player_count']

def get_players(SERVER_ADDRESS):
    try:
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()
            player_count = info['player_count']

            # players = server.players()
            # players_online = players['players']

            return player_count
    
    except:
        raise Exception("Unable to get player count")