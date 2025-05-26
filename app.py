from flask import Flask, jsonify
from cachelib import SimpleCache
import a2s
import os
import socket

app = Flask(__name__)
cache = SimpleCache()

SERVER_IP = os.environ.get("SERVER_IP", "127.0.0.1")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "27015"))
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

@app.route("/")
def info():
    cached = cache.get("server_info")
    if cached:
        return jsonify(cached)

    try:
        server_info = a2s.info(SERVER_ADDR, timeout=2.0)
        players_raw = a2s.players(SERVER_ADDR, timeout=2.0)

        players = [
            {
                "name": p.name,
                "score": p.score,
                "duration": round(p.duration, 1)
            }
            for p in players_raw if p.name
        ]

        result = {
                "name": server_info.server_name,
                "map": server_info.map_name,
                "players": server_info.player_count,
                "max_players": server_info.max_players,
                "game": server_info.game,
                "player_list": players
            }

        cache.set("server_info", result, timeout=30)
        return jsonify(result)

    except (socket.timeout, TimeoutError, Exception) as e:
        return jsonify({"error": "Server did not respond", "details": str(e)}), 504
    
@app.route('/ping')
def ping():
    return 'pong'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=27014)
