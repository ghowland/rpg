#!/usr/bin/env python


from rpg_log import Log
import rpg_gfx
import rpg_image
import rpg_player


#def GetMapOffsetTilePos(game):
#  tile_x_offset = game.map.offset[0] / TILE_SIZE
#  tile_y_offset = game.map.offset[1] / TILE_SIZE
#  
#  return [tile_x_offset, tile_y_offset]


def RenderMap(game, background):
  """Render the map"""
  TILE_SIZE = game.data['map']['tile_size']
  
  MAP_SCREEN_WIDTH = (game.core.size[0] / TILE_SIZE) + 1
  MAP_SCREEN_HEIGHT = (game.core.size[1] / TILE_SIZE) + 1
  
  tile_x_offset = game.map.offset[0]
  tile_y_offset = game.map.offset[1]
  
  #Log('Render map offset: %s, %s'  % (tile_x_offset, tile_y_offset))
  
  #TODO(g): Make screen drawing dynamic based on core.size and scrolling offsets
  for y in range(0, MAP_SCREEN_HEIGHT):
    for x in range(0, MAP_SCREEN_WIDTH):
      tile_x = tile_x_offset + x
      tile_y = tile_y_offset + y
      
      index = game.map.GetTileIndex((tile_x, tile_y))
      
      filename = game.map.GetPaletteImage(index)
      image = rpg_image.Load(filename)
      pos = (x * TILE_SIZE, y * TILE_SIZE)
      
      if game.map.CheckVisibility(tile_x, tile_y):
        rpg_gfx.Draw(image, background, pos)
      else:
        rpg_gfx.DrawBlack(background, pos, (TILE_SIZE, TILE_SIZE))
  

def RenderMapObjects(game, background):
  """Render the map"""


def RenderActors(game, background):
  """Render the map"""
  # Draw all the actors
  for name in game.map.actors:
    actor = game.map.actors[name]
    if game.map.CheckVisibility(actor.pos.x, actor.pos.y):
      rpg_gfx.Draw(actor.image, background, actor.GetScreenPos())
  
  # If the player is in the game yet...
  if game.player:
    #colorkey = game.player.data.get('image_color_key', None)
    #
    ##Log('Player: %s - %s' % (game.player.data['image'], colorkey))
    #player = rpg_image.Load(game.player.data['image'], colorkey=colorkey)
    
    rpg_gfx.Draw(game.player.image, background, game.player.GetScreenPos())


def RenderMapOverhead(game, background):
  """Render the map"""


def RenderActorsOverhead(game, background):
  """Render the map"""


def RenderMapCeiling(game, background):
  """Render the map"""


def RenderActorsSpeech(game, background):
  """Render the map"""


def RenderUI(game, background):
  """Render the map"""
  TILE_SIZE = game.data['map']['tile_size']
  
  # If we dont have a Player yet, get their name
  if game.player == None:
    ui_back = rpg_image.Load('data/ui/board_500.png')
    rpg_gfx.Draw(ui_back, background, (70,55))
    
    ui_back_slot = rpg_image.Load('data/ui/board_500_slot_61.png')
    ui_back_slot_small = rpg_image.Load('data/ui/board_500_slot_35.png')
    #rpg_gfx.Draw(ui_back_slot, background, (70+30,55+75))
    rpg_gfx.Draw(ui_back_slot, background, (70+30,55+145))
    #rpg_gfx.Draw(ui_back_slot, background, (70+30,55+215))
    #rpg_gfx.Draw(ui_back_slot, background, (70+30,55+285))
  
    
    rpg_image.DrawText('Enter your name', 35, (255, 255, 255), (100,80), background,
                       outline=1)
    
    rpg_image.DrawText(game.core.input.GetAutoString() + '|', 35, (255, 255, 255),
                       (70+30+15, 55+145+15), background, outline=1)
    
    # If we have a name entered
    if game.core.input.GetNewEnteredString():
      name = game.core.input.GetNewEnteredString()
      
      # Create the player
      game.player = rpg_player.Player(game, name)
      # The player is here, update visibility
      game.map.UpdateVisibility()
  
  # If there is a dialobue going on, render it
  if game.dialogue:
    game.dialogue.Render(background)
  
  if 0:
    # Get the cursor tile position
    pos = GetMapOffsetTilePos(game)
    pos[0] += game.mouse.pos[0] / TILE_SIZE
    pos[1] += game.mouse.pos[1] / TILE_SIZE
    
    cursor_pos = ((game.mouse.pos[0] - game.mouse.pos[0] % TILE_SIZE),
                  (game.mouse.pos[1] - game.mouse.pos[1] % TILE_SIZE))
    
    Log('Map Pos: %s = %s.  %s' % (str(pos), game.map.GetPosData(pos), str(cursor_pos)))
    
    # Draw the tile cursor
    cursor = rpg_image.Load(rpg_data.UI['cursor_tile'], colorkey=(0,255,0))
    rpg_gfx.Draw(cursor, background, cursor_pos)
  
  

