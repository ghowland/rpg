#!/usr/bin/env python

import yaml
import random

import rpg_log
from rpg_log import Log
import rpg_base
import rpg_image
import rpg_item


class Actor:
  
  def __init__(self, game, data):
    """Create the actor, place it on the map."""
    self.game = game
    self.data = data
    self.name = data['name']
    
    # Create our attributes (need to make new field references)
    self.attributes = {}
    for key in self.data.get('attributes', {}):
      self.attributes[key] = self.data['attributes'][key]
    
    # Create items
    self.items = []
    for key in self.data.get('items', {}):
      item = rpg_item.Item(self.game, self, self.data['items'][key])
      self.items.append(item)
    
    # Image
    self.image = rpg_image.Load(data['image'],
                                colorkey=data.get('image_color_key',
                                game.data['game']['color_key']))
    
    starting_position = data['pos']
    self.pos = rpg_base.Position(starting_position[0], starting_position[1])
    self.pos_last = self.pos
    
    # Save any data we need to manipulate
    self.money = data.get('money', 0)
    
    
    # More stats
    self.fatigued = False
    
    #Log('Actor data: %s' % self.data)


  def __repr__(self):
    output = 'Actor: %s\n' % self.name
    output += '  Pos: %s' % self.pos
    output += '  ---\n'
    
    keys = self.data.keys()
    keys.sort()
    for key in keys:
      output = '  %s: %s\n' % (key, self.data[key])
    
    output += '\n'
    
    return output


  def GetScreenPos(self):
    """Returns the pixel position on the screen."""
    screen_x = (self.pos.x - self.game.map.offset[0]) * \
                self.game.data['map']['tile_size']
    screen_y = (self.pos.y - self.game.map.offset[1]) * \
                self.game.data['map']['tile_size']
    
    return (screen_x, screen_y)
  

  def Update(self, ticks=0):
    """Actor AI"""
    if random.randint(0,5) == 0:
      x = random.randint(-1, 1)
      y = random.randint(-1, 1)
      self.Move(x, y)


  def Move(self, x, y):
    """x and y should be values between -1 and 1."""
    
    new_x = self.pos.x + x
    new_y = self.pos.y + y
    
    # Bound the position by the map size
    if new_x < 0:
      new_x = 0
    
    if new_y < 0:
      new_y = 0
    
    if new_x >= self.game.map.width:
      new_x = self.game.map.width - 1
    
    if new_y >= self.game.map.height:
      new_y = self.game.map.height - 1
    
    # See if we can actually move to this new position
    is_blocked = self.game.map.IsTileBlocked(new_x, new_y, self)
    
    if not is_blocked:
      # Save our last position
      self.pos_last = rpg_base.Position(self.pos.x, self.pos.y)
      
      # Update our new position
      self.pos.x = new_x
      self.pos.y = new_y
      
      # If this is the player, then do these
      if self == self.game.player:
        # Check for Map features of this tile
        self.game.map.ProcessPlayerTileMove()
        
        # After a move, ensure the map is positioned properly
        self.PostMove()
        
        # Update the visibility map
        self.game.map.UpdateVisibility()


  def PostMove(self):
    """Update things about the character."""
    #TODO(g): Move this somewhere else, this is a weird place for it, but
    #   easy now.
    screen_pos = self.GetScreenPos()
    
    # If player is off the screen, center on the player
    if self.IsOffScreen():
      Log('Player off screen: Centering')
      self.CenterToScreen()
    
    # Keep up with the player
    if screen_pos[0] < (self.game.core.size[0] * 0.30):
      self.game.map.MoveOffset(-1, 0)
    
    if screen_pos[1] < (self.game.core.size[1] * 0.30):
      self.game.map.MoveOffset(0, -1)
    
    if screen_pos[0] > (self.game.core.size[0] * 0.70):
      self.game.map.MoveOffset(1, 0)
    
    if screen_pos[1] > (self.game.core.size[1] * 0.70):
      self.game.map.MoveOffset(0, 1)
  
  
  def GetScreenPos(self):
    """Returns the pixel position on the screen."""
    screen_x = (self.pos.x - self.game.map.offset[0]) * \
                self.game.data['map']['tile_size']
    screen_y = (self.pos.y - self.game.map.offset[1]) * \
                self.game.data['map']['tile_size']
    
    return (screen_x, screen_y)
  

  def IsOffScreen(self):
    """Is the player off the screen?"""
    tiles = self.game.map.GetTilesPerScreen()
    
    if self.pos.x < self.game.map.offset[0] or \
        self.pos.x > self.game.map.offset[0] + tiles[0]:
      Log('OFF X: Player: %s  Map: %s' % (self.pos, self.game.map.offset))
      return True
    
    if self.pos.y < self.game.map.offset[1] or \
        self.pos.y > self.game.map.offset[1] + tiles[1]:
      Log('OFF Y: Player: %s  Map: %s' % (self.pos, self.game.map.offset))
      return True


  def CenterToScreen(self):
    """Center the screen on the player."""
    tiles = self.game.map.GetTilesPerScreen()
    
    self.game.map.offset[0] = self.pos.x - tiles[0] / 2
    self.game.map.offset[1] = self.pos.y - tiles[1] / 2
    
    Log('Player: %s  Map: %s' % (self.pos, self.game.map.offset))
    #
    #if self.game.map.offset[0] < 0:
    #  self.game.map.offset[0] = 0
    #if self.game.map.offset[1] < 0:
    #  self.game.map.offset[1] = 0


  def Pay(self, source_actor, target_actor, amount, reason=None):
    """Returns success of payment."""
    #TODO(g): Source actor should be this actor, should only need target.  FIX
    
    # If the source can pay, then pay
    if source_actor.money >= amount:
      source_actor.money -= amount
      target_actor.money += amount
      
      Log('%s pays %s %s: %s' % (source_actor.name, target_actor.name,
                                 amount, reason))
      return True
    
    # Else, log failure
    else:
      Log('%s FAILS to pay %s %s: %s' % (source_actor.name, target_actor.name,
                                         amount, reason))
      return False


  def ConditionCheck(self, condition):
    """Returns boolean."""
    value = None
    value_target = None
    
    # If it wants an attribute
    if 'attribute' in condition:
      value = self.attributes[condition['attribute']]
    else:
      Log('Actor: ConditionCheck: Unknown value type', status=rpg_log.LEVEL_CRITICAL)
    
    # If it wants an attribute
    if 'target_attribute' in condition:
      value_target = self.attributes[condition['target_attribute']]
    
    
    # Condition
    if 'greater_than' in condition:
      # If this is a percentage, convert the percentage item
      if '%' in condition['greater_than']:
        percent = int(str(['greater_than']).replace('%', '')) * 0.01
        value_target *= percent
      
      # Compare the values
      if value > value_target:
        return True
      else:
        return False
    else:
      Log('Actor: ConditionCheck: Unknown condition check', status=rpg_log.LEVEL_CRITICAL)
    
    
    # If it got here, it's set up wrong
    Log('Actor: ConditionCheck: No valid condition path', status=rpg_log.LEVEL_CRITICAL)
    return False

