#!/bin/bash


screen -dmS "GAMESERVER_MANAGER_SERVICE_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_gameserver_manager_xmlrpc.py"
screen -dmS "CRAFTING_SERVICE_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_crafting_service_xmlrpc.py"
screen -dmS "ITEMLIST_ENTRY_LOGGER_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_itemlist_entrylogger_xmlrpc.py"
screen -dmS "ITEM_PERSISTENCE_SERVICE_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_item_persistence_service_xmlrpc.py"
screen -dmS "PLAYER_SERVICE_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_player_service_xmlrpc.py"
screen -dmS "LOGIN_SERVICE_XMLRPC" "python" "$VIRTUAL_ENV/bin/startup_loginserver_xmlrpc.py"
screen -ls