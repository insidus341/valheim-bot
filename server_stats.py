import valve.source.a2s
# https://python-valve.readthedocs.io/en/latest/source.html

SERVER_ADDRESS = ("jamesearl.co.uk", 2457)

with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
    info = server.info()
    server_name = info['server_name']
    player_count = info['player_count']
    
    players = server.players()
    players_online = players['players']
    
    