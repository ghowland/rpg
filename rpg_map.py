#!/usr/bin/env python


import os
import yaml


import rpg_log as log
from rpg_log import Log

import rpg_image
from rpg_util import YamlOpen
import rpg_base
import rpg_actor
import rpg_dialogue


class Map:
  
  def __init__(self, game, path):
    """Load up the map."""
    self.game = game
    self.path = path
    
    self.map_filename = '%s/map.bmp' % path
    self.palette = yaml.load(YamlOpen('%s/palette.txt' % path))
    self.data = yaml.load(YamlOpen('%s/map.txt' % path))
    
    self.image = rpg_image.Load(self.map_filename, convert=False)
    
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    
    self.image_buffer = rpg_image.GetImageBuffer(self.image)
    
    #TODO(g): Convert to Position
    self.offset = [0, 0]
    
    log.Log('Map: %s,%s' % (self.width, self.height))
    
    # Visibility map: Make it true initially, to give a background to the
    #   opening UI.
    self.ClearVisibilityMap(value=1)
    
    # Create our Actors
    self.CreateActors()


  def __repr__(self):
    output = 'Map:\n'
    output += '  Path: %s\n' % self.path
    output += '  Size: (%s, %s)\n' % (self.width, self.height)
    output += '  Offset: (%s, %s)\n' % (self.offset[0], self.offset[1])
    
    output += '  ----\n'
    keys = self.data.keys()
    keys.sort()
    for key in keys:
      if key not in ('actors', 'doors', 'houses', 'scene'):
        output += '  %s = %s\n' % (key, self.data[key])
    
    return output


  def Update(self, ticks=0):
    """Update the map.  NPCs and any other events."""
    for name in self.actors:
      self.actors[name].Update(ticks=ticks)



  def CreateActors(self):
    """Create our actors."""
    self.actors = {}
    
    # If there are no actors, we're done
    if 'actors' not in self.data:
      return
    
    # Save all of the actors by their tag names
    for key in self.data['actors']:
      actor = rpg_actor.Actor(self.game, self.data['actors'][key])
      self.actors[key] = actor



  def ClearVisibilityMap(self, value=0):
    self.visibility = []
    for y in range(0, self.height):
      row = []
      self.visibility.append(row)
      
      for x in range(0, self.width):
        # Nothing is visible, by default
        row.append(value)


  def CheckVisibility(self, x, y):
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      return 0
    
    return self.visibility[y][x]


  def SetVisibility(self, x, y, value=1):
    #Log('Set vis: %s,%s' % (x, y))
    self.visibility[y][x] = value


  def UpdateVisibility(self):
    """Update what portions of the map are visible"""
    # Clear the map
    self.ClearVisibilityMap()
    
    # Only update it if we have a player
    if not self.game.player:
      return
    
    max_vis_day = self.data.get('max_visibility', self.game.data['map']['max_visibility'])
    max_vis_night = self.data.get('max_visibility_night', self.game.data['map']['max_visibility_night'])
    
    #TODO(g): Add day/night cycle
    max_vis = max_vis_day
    
    # Cast rays from the player.  Step out from the player and find the
    #   angle to the player to determine if visible.
    center = self.game.player.pos.ToList()
    
    # Check every tile
    for y in range(center[1] - max_vis, center[1] + max_vis):
      for x in range(center[0] - max_vis, center[0] + max_vis):
        dist = rpg_base.GetDistance(center, [x, y])
        # Only really test tiles that are within viewing range
        if dist <= max_vis:
          #Log('%s -> %s = %s' % (center, [x, y], dist))
          if self.game.map.HasLineOfSightToPlayer(x, y):
            self.SetVisibility(x, y)


  def GetTileIndex(self, pos):
    """Get position data for this map position."""
    #pixel = rpg_image.GetPixel(self.image, pos)
    try:
      pixel = self.image_buffer[pos[0]][pos[1]]
    except IndexError, e:
      pixel = -1
    
    return pixel


  def IsTileBlocked(self, x, y, actor_moving):
    """Returns 1 if this index blocks movement, 0 if actors can walk on it."""
    index = self.GetTileIndex([x, y])
    blocked = self.palette[index].get('blocking', 0)
    
    # If we're not blocked by an obstacle, check for an actor
    if not blocked:
      # Check against the player, if not the player
      if self.game.player and actor_moving != self.game.player and \
            self.game.player.pos.IsSame([x, y]):
        blocked = True
      
      # Check against the actors, if not the same actor
      for name in self.actors:
        actor = self.actors[name]
        if actor_moving != actor and actor.pos.IsSame([x, y]):
          blocked = True
    
    return blocked


  def IsTileBlockingView(self, x, y):
    """Returns 1 if this index blocks movement, 0 if actors can walk on it."""
    index = self.GetTileIndex([x, y])
    return self.palette[index].get('noview', 0)


  def GetPaletteImage(self, index):
    """Returns the image for the palette's index."""
    return self.palette[index]['image']


  def MoveOffset(self, x, y):
    self.offset[0] += x
    self.offset[1] += y
    
    tiles = self.GetTilesPerScreen()
    
    if self.offset[0] < 0:
      self.offset[0] = 0
    
    if self.offset[1] < 0:
      self.offset[1] = 0
    
    if self.offset[0] >= self.width - tiles[0]:
      self.offset[0] = self.width - tiles[0]
    
    if self.offset[1] >= self.height - tiles[1]:
      self.offset[1] = self.height - tiles[1]


  def GetTilesPerScreen(self):
    TILE_SIZE = self.game.data['map']['tile_size']
    
    tile_x = int(self.game.core.size[0] / TILE_SIZE)
    tile_y = int(self.game.core.size[1] / TILE_SIZE)
    
    return (tile_x, tile_y)


  def HasLineOfSightToPlayer(self, x, y):
    # If the game doenst have a player yet, it's true
    #TODO(g): Or is it false?
    if not self.game.player:
      return True
    
    # Check map boundaries
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      return False
    
    if self.game.player.pos.IsSame([x, y]):
      return True
    
    # Draw a line from here to the player,
    points = rpg_base.GetLineBetweenPositions([x, y],
                                              self.game.player.pos.ToList())
    
    # Check if any of the points from here to there (not including ends)
    #   are blocking the view.
    for point in points[1:-1]:
      if self.IsTileBlockingView(point[0], point[1]):
        #Log('%s -> (%s,%s): Blocked by %s,%s: %s\n%s' % \
        #    (self.game.player.pos, x, y, point[0], point[1],
        #     self.GetTileIndex([point[0], point[1]]), points))
        return False
    
    # Nothing is blocking the view
    return True
  

  def ProcessPlayerTileMove(self):
    """Process anything that needs to happen now that the player is on this tile.
    """
    # If the player steps on a door
    if 'doors' in self.data:
      for key in self.data['doors']:
        door = self.data['doors'][key]
        
        if self.game.player.pos.IsSame(door['pos']):
          Log('Entering door: %s: %s' % (key, door['map']))
          self.game.SelectMap(door['map'])
          
          if 'player_pos' in door:
            (player_x, player_y) = door['player_pos']
          else:
            (player_x, player_y) = self.game.map.data['player']['starting_pos']
          
          self.game.player.pos = rpg_base.Position(player_x, player_y)
          
          # Center the player on the screen
          tiles = self.game.map.GetTilesPerScreen()
          self.game.map.offset[0] = self.game.player.pos.x - tiles[0] / 2
          self.game.map.offset[1] = self.game.player.pos.y - tiles[1] / 2
    
    # Check if we have stepped next to an actor
    for name in self.actors:
      actor = self.actors[name]
      if self.game.player.pos.GetDistance(actor.pos) <= 1.0:
        self.game.dialogue = rpg_dialogue.Dialogue(self.game, actor)
        break


