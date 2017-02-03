
Survive Documentation
=====================


This is the documentation page for the survive project. I hope that it stays up to date but there surely
will be something missing over time.

For further references and information about me just look at: `Homepage <http://heleska.de/index>`_


.. toctree::
    :maxdepth: 2

    development/basics
    gdd/gdd
    testing/testing
    leveldesign/leveldesign



Notes (Just scribbels)
----------------------

h3. Crafting
* Der Server steuert die Größe des Crafting Grids
* Welche Größe des Crafting Grids der Spieler bekommt hängt von dem Objekt ab worauf er steht
* Standardtmäßig ist es ein 3x3 Grid
* Mit diversen Objekten wird dies in unterschiedlichen Shapes ausgespielt

h3. Gegenstände
* Items sind über ItemTypes/ItemTemplates definiert
* Items sind quasi nur instanzen von ItemTemplates mit einer Menge numerischer Parameter
* ItemTemplates besitzen eine Shape, Anzahl an Initialen Benutzungen und eine Menge von Tags
** Initiale Benutzungen - 0/Kein verbrauch - > 0 Anzahl usages

h3. Wearing System
* Items haben über ihr ItemTemplate eine Menge von Tags - der Tag <Wearable> gibt dabei an das etwas angezogen werden kann
* Wenn ein ItemTemplate das Tag <Wearable> hat muss es genau einen Slot Tag definieren, welcher beschreibt, wo das Item angezogen werden kann
* Die Menge der Slot Tags ist [<Hand>, <Mask>, tbd.]

h3. Objekte
* Objekte im Level werden derzeit über den LevelEditor in der Welt platziert und haben gewisse Attribute die mitgegeben werden können
* Mögliche Attribute
** searchable
*** initial_content [(item_type_id, amount), (item_type_id, amount), ...]
*** tbd. irgendeine art von tags für das anchspawnen
** collidable
*** Wenn das Objekt sichtbar ist, ist das über den mittleren Fußpunkt Referenzierte Tile nicht walkable
** stepable
*** Ist quasi für bodenplatten o.ä. reserviert - wenn der spieler darauf steht ist diese aktiviert

h3. SteppingRule
* Derzeit bezieht sich eine Stepping Rule auf eine Menge von stepable objects und eine Menge von Objects die invisible werden wenn alle stepables aktiv sind
** TODO - Komplexere logische Puzzle

h3. Item Spawning
ItemSpawning: -> Wenn ein Spot gelootet ist, wird ein timer gesetzt -> Respawn hat zwei bedingungen
** 1. Timer ist abgelaufen
** 2. Keine Spieler sind mehr in dem raum

h3. Object Interaction
h3. Item Using


h3. Object Creation (Item -> Object Duality)


Roboterspawner (Versorgunsschächte)


Spieler können sich frei bewegen (durcheinander durch)


Ducken möglich

Batterien fürs Türschloss



Next Steps:

Programming
- A* - Zombies den Gegner approachen -> moved


Writing
- Klappentext

Creative
- Gegnerdesign
- Grundlegende Übersicht für Räume / Grobkonzept der Levelzusammenghörigkeit (Adijazenz)
- Grundlegender Itemtree/Techtree


Für ItemSystem:
* Es gibt Negative Modifier (Effekt, Typisierung)
* Items Haben Typisierung
* Negative Modifier können auf Items landen (bei benutzung) wenn sie den entsprechenden ihrem Typ besitzten oder den Zerlungskomponententypen







