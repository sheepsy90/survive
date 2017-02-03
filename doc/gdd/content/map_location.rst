Map & Locations
===============

The map is divided into a set of rooms which are technically a separate game instance each. This allows for easy
scalability and even the possibility of multiple mirrored instances which can distribute load easily if there is some.

In general the maps consist of a safe zone main room where all players will arrive on start. All other rooms are not
considered safe in the beginning but can be secured by the players. How exactly rooms are secured will be explained in
the game systems part. The rooms are roughly round about from 20x20 to 100x100 tiles in size and can have various
shapes. The properties which rooms can have are the following:

Temperature
***********
Temperature is the property which describes the heat conditions in a room. Low or high temperatures can cause certain
status effects while in this room and therefore are an additional way of adding puzzle complexity.

Atmosphere
**********
As described in the intro the game takes place at a damaged arcology which results in some of the rooms beeing
exposed to the outside atmosphere in the future setting. Rich in carbon dioxide and methane as well as other
not really healthy gases it can harm the player when exposed. The atmosphere property now describes whether there
is outside atmosphere present or if there is the filtered air still provided by the arcology system. There is also in
this category the possibility to add other states later on to provide more puzzle complexity.

Puzzle Character
****************
To enhance the player experience the rooms shall not only provide a place to scavenge loot and to explore and enhance
the game world - some of the rooms shall also rely on difficult multiplayer puzzles to be solved in order to progress
further and explore hidden and other rooms of the arcology.

To give the player a chance to get the hang of the easier puzzles there will be a "training area" which doesn't pose a
threat to the players but don't yield much valuable stuff.

