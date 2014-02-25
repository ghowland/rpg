#!/usr/bin/env python

"""
RPG: BarterSell

Bartering for selling things to an actor.
"""


class BarterSell:
  
  def __init__(self, game, dialogue, data):
    self.game = game
    self.dialogue = dialogue
    self.data = data
    
    self.selected_option = 0
    
    # This is 
    self.option_offset = 0
    
    # Options for our bartering
    self.options = []
    
    # Initialize our options
    self.Initialize()


  def Initialize(self):
    """Initialize our options from our data."""
    


  def Update(self, ticks=0):
    """Do something with updating the barter.  Not really necessary now."""
    
  
  
  def Render(self, background):
    """Draw the barter on the background."""
    ui_back = rpg_image.Load('data/ui/board_500.png')
    rpg_gfx.Draw(ui_back, background, (70,55))
    
    ui_back_slot = rpg_image.Load('data/ui/board_500_slot_61.png')
    ui_back_slot_small = rpg_image.Load('data/ui/board_500_slot_35.png')
    
    # Print option background borders
    if len(self.options) >= 1:
      rpg_gfx.Draw(ui_back_slot, background, (70+30,55+75))
    if len(self.options) >= 2:
      rpg_gfx.Draw(ui_back_slot, background, (70+30,55+145))
    if len(self.options) >= 3:
      rpg_gfx.Draw(ui_back_slot, background, (70+30,55+215))
    if len(self.options) >= 4:
      rpg_gfx.Draw(ui_back_slot, background, (70+30,55+285))
    
    # Draw the Prompt
    rpg_image.DrawText(self.prompt, 30, (255, 255, 255), (100,80), background,
                       outline=1)
    
    # Print all the option texts
    for count in range(0, len(self.options)):
      #TODO(g): Make the show_always data option check and force this option
      #   to be the last option, if we have it set to be on
      
      # Only drawing 4 now
      if count >= 4:
        break
      
      option = self.options[count]
      
      x = 70+30 + 15
      y = 55+75 + (70 * count) + 15
      
      # If this option is selected, highlight it
      if self.selected_option == count:
        color = (255, 0, 0)
      else:
        color = (255, 255, 255)
      
      rpg_image.DrawText(option['text'], 20, color, (x,y), background,
                         outline=1)


  def HandleInput(self, input):
    """Handle any input for getting through our dialogue options."""
    if input.IsKeyDown(K_UP, once=True):
      self.selected_option -= 1
      if self.selected_option < 0:
        self.selected_option = len(self.options) - 1
    if input.IsKeyDown(K_DOWN, once=True):
      self.selected_option += 1
      if self.selected_option >= len(self.options):
        self.selected_option = 0
    
    # Selection
    if input.IsKeyDown(K_RETURN, once=True):
      self.SelectSpeechOption()


