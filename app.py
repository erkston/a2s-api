from flask import Flask, request, jsonify
from cachelib import SimpleCache
import a2s
import socket

app = Flask(__name__)
cache = SimpleCache()

@app.route("/query", methods=["POST"])
def query_server():
    data = request.get_json()
    if not data or "ip" not in data or "port" not in data:
        return jsonify({"error": "Missing 'ip' or 'port' in request body"}), 400

    ip = data["ip"]
    port = int(data["port"])
    server_addr = (ip, port)

    cache_key = f"server_info_{ip}_{port}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached)

    try:
        server_info = a2s.info(server_addr, timeout=2.0)
        players_raw = a2s.players(server_addr, timeout=2.0)
        rules = a2s.rules(server_addr, timeout=2.0)

        players = [
            {
                "name": p.name,
                "score": p.score,
                "duration": round(p.duration, 1)
            }
            for p in players_raw if p.name
        ]

        result = {
            "server_name": server_info.server_name,
            "map_name": server_info.map_name,
            "folder": server_info.folder,
            "game": server_info.game,
            "app_id": server_info.app_id,
            "player_count": server_info.player_count,
            "max_players": server_info.max_players,
            "bot_count": server_info.bot_count,
            "server_type": server_info.server_type,
            "platform": server_info.platform,
            "password_protected": server_info.password_protected,
            "vac_enabled": server_info.vac_enabled,
            "version": server_info.version,
            "edf": server_info.edf,
            "game_id": server_info.game_id,
            "keywords": server_info.keywords,
            "player_list": players,
            "rules": rules
        }

        cache.set(cache_key, result, timeout=30)
        return jsonify(result)

    except (socket.timeout, TimeoutError, Exception) as e:
        return jsonify({"error": "Server did not respond", "details": str(e)}), 504

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=27014)
