# A2S API

This Project uses [python-a2s](https://github.com/Yepoleb/python-a2s) and
Flask to create a query REST API for Source Dedicated Servers. Forked from [spezifanta/hlds-api](https://github.com/spezifanta/hlds-api).

## Usage

The script/container no longer requires ENV variables for the server IP/port you want to query. It now receives the server info in the POST.

### Docker

See [compose.yml.example](compose.yml.example)

### Manual

```bash
python app.py
```

This will create webserver on port `27014`.

## Endpoints

### `/query`

URL encoded parameters or json body are accepted:

```
curl -X GET "http://127.0.0.1:27014/query?ip=chi-1.us.uncletopia.com&port=27015"
```

or:

Headers:

```
Content-Type: application/json
```

Body:

```json
{
  "ip": "chi-1.us.uncletopia.com",
  "port": 27015
}
```

#### Response

```json
{
    "player_list": [
        {
            "duration": 6095.1,
            "name": "sickomode123",
            "score": 10
        },
        {
            "duration": 4492.2,
            "name": "troll",
            "score": 37
        },
        ...
    ],
    "rules": {
        "centerprojectiles_version": "8.0",
        "coop": "0",
        "deathmatch": "1",
        "decalfrequency": "10",
        "discord_accelerator_version": "1.0",
        "discord_version": "1.0",
        "extendedmapconfig_version": "1.1.1",
        "metamod_version": "1.12.0-dev+1211V",
        "mp_allowNPCs": "1",
        "mp_autocrosshair": "1",
        "mp_autoteambalance": "0",
        "mp_disable_respawn_times": "0",
        "mp_fadetoblack": "0",
        "mp_falldamage": "0",
        "mp_flashlight": "0",
        "mp_footsteps": "1",
        ...
        
    },
    "server_info": {
        "app_id": 440,
        "bot_count": 0,
        "edf": 241,
        "folder": "tf",
        "game": "Team Fortress",
        "game_id": 440,
        "keywords": "nocrits,nodmgspread,payload,uncletopia",
        "map_name": "pl_badwater",
        "max_players": 24,
        "password_protected": false,
        "ping": 0.02306730000054813,
        "platform": "l",
        "player_count": 24,
        "port": 27015,
        "protocol": 17,
        "server_name": "Uncletopia | Chicago | 1 | All Maps",
        "server_type": "d",
        "steam_id": 85568392924469984,
        "stv_name": "Uncletopia | Chicago | 1 | All Maps | STV",
        "stv_port": 27016,
        "vac_enabled": true,
        "version": "9742990"
    }
}
```

### `/ping`

Used as healthcheck for Docker.

#### Response

```
pong
```
