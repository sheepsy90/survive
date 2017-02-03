#!/bin/bash

sudo apt-get install python-virtualenv python-dev

virtualenv .game
. .game/bin/activate

pip install numpy
pip install sphinx
