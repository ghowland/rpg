#!/usr/bin/env python

"""
RPG: Game

All the game related things work through this object.
"""


import rpg_log as log
from rpg_log import Log
import rpg_map
import rpg_render
import rpg_base




# These are all the layers we will draw
RENDER_LAYERS = {0:{'name':'Background', 'func':rpg_render.RenderMap},
                 1:{'name':'Objects', 'func':rpg_render.RenderMapObjects},
                 2:{'name':'Actors', 'func':rpg_render.RenderActors},
                 3:{'name':'Overhead', 'func':rpg_render.RenderMapOverhead},
                 4:{'name':'Overhead Actor', 'func':rpg_render.RenderActorsOverhead},
                 5:{'name':'Ceiling', 'func':rpg_render.RenderMapCeiling},
                 6:{'name':'Speech', 'func':rpg_render.RenderActorsSpeech},
                 7:{'name':'UI', 'func':rpg_render.RenderUI},
                }


class Mouse:
  def __init__(self):
    self.pos = [0, 0]
    self.buttons = [False, False, False]
  
  
  def SetPos(self, pos):
    self.pos = list(pos)
  
  
  def SetButtons(self, buttons):
    self.buttons = list(buttons)


class Game:
  """All things game related are stored here, as the central object."""
  
  def __init__(self, core, data):
    """Reset all the data."""
    self.core = core
    self.core.SetGame(self)
    
    # Data from the YAML file
    self.data = data
    
    # Create the mouse object
    self.mouse = Mouse()
    
    # Our map dictionary
    self.maps = {}
    
    #TODO(g): Make map loading dynamic
    #self.map = rpg_map.Map(self, MAP_HARDCODED)
    self.SelectMap(data['game']['initial_map'])
    
    # We're just getting started!
    self.quitting = False
    
    # For the editor-cursor: mouse
    self.cursor_map_pos = rpg_base.Position()
    
    # Player object goes here
    self.player = None
    
    # Save dialogue stuff going on.
    #TODO(g): This is cheating for having a game state stack, which I should do
    #   but will put off because it will take longer and I want NPC dialogue
    #   NOW!!!
    self.dialogue = None
    
    # When this list is non-null, the player and listed characters are battling
    self.combat = []


  def __repr__(self):
    output = 'Game:\n'
    output += '  Maps: %s\n' % self.maps.keys()
    
    output += '  ----\n'
    keys = self.data.keys()
    keys.sort()
    for key in keys:
      output += '  %s = %s' % (key, self.data[key])
    
    return output


  def SelectMap(self, map_path):
    # If we dont have this map cached, load and cache it
    if map_path not in self.maps:
      self.map = rpg_map.Map(self, map_path)
      self.maps[map_path] = self.map
    
    # Else, just use what we already had cached
    else:
      self.map = self.maps[map_path]


  def Update(self, ticks=None):
    """Update the game state.  ticks are milliseconds since last updated."""
    # Update the player, if they exist
    if self.player:
      self.player.Update(ticks=ticks)
    
    # Update the map
    self.map.Update(ticks=ticks)


  def Render(self, background):
    """Render the game, layer by layer."""
    num_layers = len(RENDER_LAYERS)
    
    # Render all the layers, in order
    for layer in range(0, num_layers):
      RENDER_LAYERS[layer]['func'](self, background)
