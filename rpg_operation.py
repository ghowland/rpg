#!/usr/bin/env python

"""
RPG: Operation

These are any operations we want to carry out from our YAML files.  Operations
are strings that are tied to Python code, to carry out things that arent
possible to easily make YAML tags for directly.
"""


from rpg_log import Log
import rpg_combat


def HandleOperation(game, operation, data):
  """Handle the operation.
  
  Args:
    game: Game object
    operation: string, name of the operation to look up
    data: dict, data at the level the operation was specified in, which may
        contain information the operation needs to operate.  Operation specific.
  """
  # Pay for a room's night sleep
  if operation == 'RoomSleepPay':
    Log('RoomSleepPay: You are rested!')
    
    # Max up the player's current health
    #NOTE(g): Uses a percentage based increase from the game data.  If not
    #   present, assume full recovery.
    modifier = game.data['game'].get('sleep_regeneration_percent', 1.0)
    
    # Add the modified version of the full health
    game.player.health_current += game.player.attributes['health'] * modifier
    
    # Max out at full health
    if game.player.health_current > game.player.attributes['health']:
      game.player.health_current = game.player.attributes['health']
    
    # No longer fatigued (running and such)
    game.player.fatigued = False
  
  
  # Combat with the Player
  elif operation == 'CombatPlayer':
    if game.dialogue:
      # If a map is specified for the encouter, then fight
      map = data.get('map', None)
      
      # Set combat to be with the given actor
      game.combat = rpg_combat.Combat(game, [game.dialogue.actor], map=map)
      
      # Clear the dialogue.  The time for talking is OVER!
      game.dialogue = None
    else:
      Log('Operatino: CombatPlayer: Not initiated from Dialogue.  Unknown actor.')
  
  
  # Close the Dialogue
  if operation == 'CloseDialogue':
    game.dialogue = None
  
  
  

