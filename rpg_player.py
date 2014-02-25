#!/usr/bin/env python

import yaml

import rpg_log as log
from rpg_log import Log
import rpg_base
import rpg_actor
import rpg_image
from rpg_util import YamlOpen
import rpg_item


DATA_FILE = 'data/general/player.txt'


class Player(rpg_actor.Actor):
  
  def __init__(self, game, name):
    """Create the player, place it on the map."""
    self.game = game
    self.name = name
    
    starting_position = game.map.data['player']['starting_pos']
    self.pos = rpg_base.Position(starting_position[0], starting_position[1])
    self.pos_last = self.pos
    #TODO(g): Unhard-code the default player
    self.data = yaml.load(YamlOpen(DATA_FILE))['default']
    
    # Image
    self.image = rpg_image.Load(self.data['image'],
                    colorkey=self.data.get('image_color_key',
                        game.data['game']['color_key']))
    
    
    # Save any attributes we want specifically out of our data
    self.money = self.data.get('money', 0)
    
    # Create our attributes (need to make new field references)
    self.attributes = {}
    for key in self.data.get('attributes', {}):
      self.attributes[key] = self.data['attributes'][key]
    
    # Create our items
    self.items = []
    for key in self.data.get('items', {}):
      item = rpg_item.Item(self.game, self, self.data['items'][key])
      self.items.append(item)
    
    # Save the current health of the player
    if 'heath' in self.attributes:
      self.health_current = self.attributes['health']
    else:
      #NOTE(g): This makes the player alive.  Apparently health isnt important
      #   in this game...
      self.health_current = 1
    
    # Get the quests we start with
    #TODO(g): Make this a deep copy, so we arent changing the data we loaded
    self.quests = dict(self.data['quests'])
    
    # Save the current health of the player
    if 'mana' in self.attributes:
      self.mana_current = self.attributes['mana']
    else:
      #NOTE(g): Mana is not necessary, like health i
      self.mana_current = 0
    
    # More stats
    self.fatigued = False
    
    # Achievements
    self.achievements = {}


  def __repr__(self):
    output = 'Player: %s\n' % self.name
    output += '  Pos: %s\n' % self.pos
    output += '  Money: %s\n' % self.money
    output += '  Achievements\n    %s\n\n' % self.achievements.keys()
    output += '  Quests:\n    %s\n\n' % self.quests.keys()
    
    output += '  Items:\n'
    for item in self.items:
      output += '%s\n\n' % str(item)
    
    return output
  
  
  def Update(self, ticks=0):
    """Update things about the character."""
    
  
