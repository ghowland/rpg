#!/usr/bin/env python

"""
RPG: Core

This is the core of the RPG.  All graphics, sound, windows, input
and all other non-game stuff happens here.
"""


import pygame
from pygame.locals import *


import rpg_log as log
from rpg_log import Log
import rpg_image
import rpg_input


class Core:
  """The core.  All non-game related functions wrapped here."""
  
  def __init__(self, title, size):
    """Initialize the core information."""
    self.title = title
    self.size = size
    self.game = None
    
    # Initialize the Graphics stuff
    #NOTE(g): This creates self.screen
    rpg_image.InitializeGraphics(self)
    
    # Create the background surface
    self.background = pygame.Surface(size)
    self.background = self.background.convert()
    self.background.fill((250, 250, 250))
    
    # Create Input Handler
    self.input = rpg_input.InputHandler()


  def Update(self, ticks=None):
    """Update everything."""
    self.game.Update(ticks=ticks)


  def HandleInput(self, game):
    """Handle input"""
    # Save the mouse position
    game.mouse.SetPos(pygame.mouse.get_pos())
    
    # Save the mouse button state (used for draw actions, use events for button
    #   down events (single fire))
    game.mouse.SetButtons(pygame.mouse.get_pressed())
    
    # Handle events through the Input Handler
    self.input.Update()
    
    #if self.input.GetAutoString():
    #  log.Log('Auto string: %s' % self.input.GetAutoString())
    
    entered_string = self.input.GetNewEnteredString()
    if entered_string:
      log.Log('Entered string: %s' % entered_string)
    
    #TODO(g): Create named input maps, which make the right function calls off
    #   of inputs.  Then we can switch which maps we're using as the game state
    #   changes, so for menus or playing or combat, or whatever.
    
    # Get player movement, if we're not in a dialogue
    #TODO(g): Switch to key maps instead and just switch keymaps along with the
    #   rendering options.
    if not game.dialogue and not game.combat:
      MOVE_ONCE = False
      if self.input.IsKeyDown(K_UP, once=MOVE_ONCE):
        if game.player:
          game.player.Move(0, -1)
      if self.input.IsKeyDown(K_DOWN, once=MOVE_ONCE):
        if game.player:
          game.player.Move(0, 1)
      if self.input.IsKeyDown(K_LEFT, once=MOVE_ONCE):
        if game.player:
          game.player.Move(-1, 0)
      if self.input.IsKeyDown(K_RIGHT, once=MOVE_ONCE):
        if game.player:
          game.player.Move(1, 0)
      
      # Get information
      if self.input.IsKeyDown(K_i, once=True):
        #Log('Game:\n%s' % self.game)
        Log('Map:\n%s' % self.game.map)
        Log('Player:\n%s' % self.game.player)
      
      # If they hit ESC
      if self.input.IsKeyDown(K_ESCAPE, once=True):
        game.quitting = True
    
    # Else, there is combat going on
    elif game.combat:
      game.combat.HandleInput()
    
    # Else, there is dialogue going on, handle that
    elif game.dialogue:
      game.dialogue.HandleInput(self.input)
    
    
    # If they are closing the window
    if self.input.winClose:
      game.quitting = True
  
  
  def Render(self, game):
    """Handle input"""
    game.Render(self.background)
    
    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()


  def SetGame(self, game):
    self.game = game


