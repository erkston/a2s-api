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
            "server_info": server_info,
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
