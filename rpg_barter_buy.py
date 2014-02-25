#!/usr/bin/env python

"""
RPG: BarterBuy

Bartering for buying things from an actor.
"""


from pygame.locals import *
import copy


from rpg_log import Log
import rpg_image
import rpg_gfx
import rpg_item



class BarterBuy:
  
  def __init__(self, game, dialogue, data):
    self.game = game
    self.dialogue = dialogue
    
    # Get the data from the Actor's data, by name
    self.data = data
    
    self.selected_option = 0
    
    # This is our option offset
    self.option_offset = 0
    
    # Options for our bartering
    self.options = []
    
    # Inventory list goes here
    self.inventory = []
    
    # Initialize our options
    self.Initialize()


  def Initialize(self):
    """Initialize our options from our data."""
    # Get the inventory out of our data, and put into our list
    self.inventory = []
    
    # For each selling group
    for group_key in self.data:
      group_name = self.data[group_key].get('name', 'Unknown')
      
      # For all our items
      for item_key in self.data[group_key]['items']:
        #TODO(g): Deal with stock levels later...
        
        item_data = copy.deepcopy(self.data[group_key]['items'][item_key]['item'])
        item_data['group_name'] = group_name
        
        # Create our item
        item = rpg_item.Item(self.game, None, item_data)
        
        # Add it to our list
        self.inventory.append(item)
    
    # Reset options
    self.options = []
    
    # Create options from inventory
    for item in self.inventory:
      text = '%s - %s - %s gold' % (item.data['name'], item.data['group_name'],
                                    item.data['cost'])
      option = {'text':text, 'item':item, 'operation':'buy'}
      
      self.options.append(option)
    
    # Add the Quit option
    option = {'text':'Done Bartering', 'operation':'done'}
    self.options.append(option)
    
    # Constrain maximum offset position
    if self.selected_option >= len(self.options):
      self.selected_option = len(self.options) - 1


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
    rpg_image.DrawText(self.dialogue.prompt, 30, (255, 255, 255), (100,80),
                       background, outline=1)
    
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
      self.SelectOption()
    
    # If they hit ESC, leave bartering
    if input.IsKeyDown(K_ESCAPE, once=True):
      Log('Quick removed barter from dialogue.')
      self.dialogue.SelectLastConversation()



  def SelectOption(self):
    """Select the current option."""
    option = self.options[self.selected_option]
    
    # If we're done bartering
    if option['operation'] == 'done':
      Log('Removed barter from dialogue.')
      self.dialogue.SelectLastConversation()
    
    
    # Else, if were buying
    elif option['operation'] == 'buy':
      item = option['item']
      reason = 'Buying: %s' % item.data['name']
      Log(reason)
      
      success = self.game.player.Pay(self.game.player, self.dialogue.actor,
                                     item.data['cost'], reason=reason)
      if success:
        # Player gains item
        Log('Player gains item: %s' % option['text'])
        self.game.player.items.append(item)
        
        #TODO(g): Seller loses item.  Count is updated.  If no more items, removed from options.
        
        # Recalculate options
        self.Initialize()
      else:
        #TODO(g): Make this dynamic.  And rotate, like the openers.
        self.prompt = 'You cant afford that.'
    
    
    # Else, error
    else:
      Log('Unknown selection operation: %s' % option)
