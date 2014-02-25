#!/usr/bin/env python

"""
RPG: Start!
"""

import yaml

import rpg_core
import rpg_game
from rpg_log import Log
import rpg_timer
from rpg_util import YamlOpen


GAME_DATA = 'data/general/game.txt'


def main():
  data = yaml.load(YamlOpen(GAME_DATA))
  
  #core = rpg_core.Core(GAME_TITLE, SCREEN_SIZE)
  core = rpg_core.Core(data['window']['title'], data['window']['size'])
  
  # Create the game
  game = rpg_game.Game(core, data)
  
  Log('Starting game...')
  while not game.quitting:
    rpg_timer.LockFrameRate(60)
    core.Update()
    core.HandleInput(game)
    core.Render(game)
  
  Log('Quitting.')


if __name__ == '__main__':
  main()

