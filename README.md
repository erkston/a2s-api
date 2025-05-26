# A2S API

This Project uses [python-a2s](https://github.com/Yepoleb/python-a2s) and
Flask to create a query REST API for Source Dedicated Servers. Forked from [spezifanta/hlds-api](https://github.com/spezifanta/hlds-api).

## Usage

### Docker

See [compose.yml.example](compose.yml.example)

### Manual

Set `SERVER_IP` and `SERVER_PORT` to the gameserver you would like to montior.

```bash
export SERVER_IP="nyc-1.us.uncletopia.com"
export SERVER_PORT="27015"
python app.py
```

This will create webserver on port `27014`.

## Endpoints

### `/`

Request basic server information including a player list.

#### Response

```json
{
    "game": "Team Fortress",
    "map": "koth_harvest_final",
    "max_players": 24,
    "name": "Uncletopia | Chicago | 1 | All Maps",
    "player_list": [
        {
            "duration": 157.5,
            "name": "BattleMedic44",
            "score": 3
        },
        {
            "duration": 140.5,
            "name": "unknown_gamer",
            "score": 0
        }
    ],
    "players": 2
}
```

### `/ping`

Used as healthcheck for Docker.

#### Response

```
pong
```
