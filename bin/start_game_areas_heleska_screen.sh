#!/bin/bash
screen -dmS "COMMON_ROOM"       "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "heleska.de" "60006" "6"
screen -dmS "TWO_PLAYER_PUZZLE" "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "heleska.de" "60008" "8"
sleep 1
screen -ls