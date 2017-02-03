#!/bin/bash

#python $VIRTUAL_ENV/bin/game_server_instance.py 0.0.0.0 60001 1
#python $VIRTUAL_ENV/bin/game_server_instance.py 0.0.0.0 60003 3
#python $VIRTUAL_ENV/bin/game_server_instance.py 0.0.0.0 60006 6

#screen -dmS "TUTORIAL_AREA_3"   "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "61003" "3"

#screen -dmS "AFTER_TUT_AREA"    "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "60001" "1"
#screen -dmS "LEFT_OF_THAT"      "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "60004" "4"
#screen -dmS "RIGHT_OF_THAT"     "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "60005" "5"
screen -dmS "COMMON_ROOM"       "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "60006" "6"
screen -dmS "TWO_PLAYER_PUZZLE" "python" "$VIRTUAL_ENV/bin/game_server_instance.py" "0.0.0.0" "60008" "8"



sleep 1
screen -ls