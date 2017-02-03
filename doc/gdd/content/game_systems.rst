Game Systems & Mechanics
========================

Health
------
    The health system is not presented in the usual way. It rather consists of a attribute based description of the
    characters current state. This allows especially for easy introduction of new status effects either positive or
    negative. Furthermore the health states allow for self boosting worsening of effects like ongoing blood loss.
    Increasing thirst due to vomit or blood loss when draining blood for a transfusion. There shall be certain status
    effects which are stackable and by that introduce a degree of severity.

Dying
-----
    The question of dying is a problematic one due to the fact that it is not entirely clear by now what this means in
    detail. Without dying the health system as well as the robots won't be a thread such that it is necessary in
    some form.

ID-Cards
--------
    The means of authorizing and moving within the arcology are realized with the use of ID Cards which can be found
    throughout the game. Those cards have a specific level ranging from zero to three for the four categories: security,
    technician, administration and science. Electric door locks throughout the station can only be opened when the player
    is in possession of an ID Card with certain level properties. Especially multiple door locks for one door force the
    player to cooperate with other players to enter specific areas.

Crafting
--------
    The server decides how big the crafting grid is which is presented to the player. This mainly depends on the object the
    player is currently standing on. Normally there is only a very small crafting grid for to-go. The player can use
    any items he like to craft new things and when there is no existing recipe the player is requested to type a
    description of what he tried to make. He then gets a dummy item which is replaced by the item itself when we decide
    to introduce that into the game. The players which came up with this recipe are then rewarded in some way. Maybe even
    on a website as founder of this recipe. This shall lead to community based crafting recipe generation.

Tag System
----------
    Item Templates (same as Item Types) are given a set of Tags when created. Those tags define certain properties and
    almost all reasoning within the game is performed by looking at those item tags.

Wearing System
--------------
    The character is able to wear certain items which gives him some advantages in certain situations. For an item type
    to become wearable it needs a <Wearable> Tag. Furthermore it needs a tag defining the slot it goes to. This
    is currently <Hand> or <Mask>.

Item Types & Looting
--------------------
    The items types are given with certain properties like a shape and a specific number of usages. The usage ranges from
    zero meaning usable as often as the player likes to a number n decreasing every use until the item vanishes. Items
    contain a specific notation of a path like in classic file systems and contain furthermore a level integer.
    This allows for easily definition of spawn packages which could be for example like:

        - /medical/basic/* 1
        - /food/snacks/* 1
        - /drinks/can/coke

    With this it is easy to allow spawning even such things as randomly spawning higher or lower levels or even go up and
    down to another branch of the item type definition tree to have similar loot also spawning in a container with a very
    low probability.


Puzzles
*******

    One of the main focuses of the game should be the puzzle character. There are many ways that could result in interesting
    puzzles to get through rooms. From the simple thing like opening a set of doors in a specific order to more complicated
    things like multiplayer puzzles which even depend on timing or something like that.

    Combining this with the element of item crafting results even in puzzles that depend on those items. In rare cases
    it could be even puzzles which are currently unsolvable util someone comes up with an item that will solve this puzzle.
    This could be for example an artificial weight that needs to be placed on a stepable plate.


