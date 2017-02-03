Technical Requirements
**********************

    The game is based on the python programming language using pygame with its bindings to the SDL library. Furthermore
    it uses XMLRPC on the server side where each system part which is responsible for storing data permanently is realized
    as a service which takes method calls from the game server instance. Each game server instance serves one level and handles
    all events going on in that level. This leads to a good scalability in terms of player capacity. For level generation
    we use the Tiled Level Editor.