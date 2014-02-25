#!/usr/bin/env python

"""
RPG: Dialogue
"""


from pygame.locals import *
import random

from rpg_log import Log
import rpg_log
import rpg_image
import rpg_gfx
import rpg_operation
import rpg_barter_buy


class Dialogue:
  
  def __init__(self, game, actor):
    self.game = game
    self.actor = actor
    
    self.player = game.player
    
    # This holds where we are in our conversations
    self.conversation_stack = []
    
    self.SelectConversation(actor.data['starting_conversation'])
    
    # If there is an action that needs to be approved, created an Approval
    #   object, and set it here.  Then the UI can handle rendering that
    #   and taking action on the data/operation if it is approved.
    #TODO(g): Leaving this here for future reference, initially Im not going
    #   to ask for approval, if they select it, they get it.  Later I may
    #   add this to make UI nicer, but its a game.  Selecting properly is part
    #   of the game.
    self.approval = None
    
    # When set, this is a Barter object, and takes over the rendering and
    #   controls to handle bartering.  This could be it's own thing, but it
    #   makes sense to work it in through Dialogue options to me.  It could be
    #   the primary dialogue, as the Dialogue will set it up by it's data.
    self.barter = None


  def SelectConversation(self, conversation):
    """Select a new conversation."""
    self.current_conversation = conversation
    self.current_converation_data = self.actor.data['conversations'][self.current_conversation]
    
    self.openers = self.current_converation_data.get('openers', None)
    self.questions = self.current_converation_data.get('questions', None)
    
    self.opener_count = 0
    self.selected_option = 0
    
    # This holds where we are in our conversations
    self.conversation_stack.append(conversation)
    
    # Clear bartering and other sub-systems
    self.barter = None
    
    # Get our new conversation prompt and options
    self.GetOpenerPrompt()
    self.GetOptions()


  def SelectLastConversation(self):
    """Select the last conversation."""
    self.conversation_stack.pop()
    
    # Select the last conversation
    self.SelectConversation(self.conversation_stack[-1])



  def GetOpenerPrompt(self):
    """Get the opening prompt, from the options."""
    if self.openers:
      keys = self.openers.keys()
      keys.sort()
      # Select the current opener prompt, from the list, in order
      self.prompt = self.openers[self.opener_count % len(keys)]
      
      # Increment opener counter, forever because we modulate the count
      self.opener_count += 1
    else:
      # Empty prompt
      self.prompt = ''
  
  
  def GetOptions(self):
    """Get all the options for this actor."""
    self.options = []
    
    # If we have questions, select them as options
    if self.questions:
      keys = self.questions.keys()
      keys.sort()
      for key in keys:
        option = self.questions[key]
        
        condition_failed = False
        
        # If we have conditions
        if 'condition' in option:
          condition = option['condition']
          
          # If the player shouldnt have this quest for this option, but does
          if 'no_quest' in condition and condition['no_quest'] in self.player.quests:
            condition_failed = True
          
          # If the player shouldnt have this achievement for this option, but does
          if 'no_achievement' in condition and condition['no_achievement'] in self.player.achievements:
            condition_failed = True
        
        # If no conditions have failed, add this option
        if not condition_failed:
          self.options.append(option)
    
    
    # Else, Barter: Buy
    elif self.current_converation_data.get('operation') == 'BarterBuy':
      # Get the inventory data for this bartering
      inventory_data = self.actor.data[self.current_converation_data['data']]
      
      # Create the barter object (handles input and rendering)
      self.barter = rpg_barter_buy.BarterBuy(self.game, self, inventory_data)
    
    
    # Else: Fail
    else:
      msg = 'Dont know how to handle this dialogue: %s' % \
            self.current_converation_data
      raise Exception(msg)
    
    #Log('Dialogue options: %s' % self.options)
  
  
  def Update(self, ticks=0):
    """Do something with updating the dialogue.  Not really necessary now."""
    
  
  
  def Render(self, background):
    """Draw the dialogue on the background."""
    # If we are bartering, render there and return
    if self.barter:
      self.barter.Render(background)
      return
    
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
    # If we are bartering, handle input there and return
    if self.barter:
      self.barter.HandleInput(input)
      return
    
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
    
    # If they hit ESC, remove the dialogue.  It's a quick escape.
    if input.IsKeyDown(K_ESCAPE, once=True):
      Log('Quick removed dialogue.')
      self.game.dialogue = None


  def SelectSpeechOption(self):
    """Currently selected option is selected."""
    option = self.options[self.selected_option]
    
    # Fill Prompt with Response to this option
    if 'response' in option:
      self.prompt = option['response']
    
    # Assume payment has not failed...
    #TODO(g): If other things cause failures, can wrap these up into an
    #   anything-fails-we-all-fail variable, but for now its coded in each
    #   additional option, as all are assumed to need payment to be filled
    #   if it is to go through.
    payment_failed = False
    
    # Pay for some information/service
    if 'cost' in option:
      #NOTE(g): Payment success and details are logged in that function
      success = self.game.player.Pay(self.game.player, self.actor,
                                     option['cost'],
                                     reason=option.get('operation', '*COST*'))
      
      if not success:
        payment_failed = True
        default = 'You dont have the money.'
        self.prompt = option.get('response_fail', default)
    
    
    # Run an operation, and the payment hasnt failed
    if 'operation' in option and not payment_failed:
      Log('Running operation: %s' % option['operation'])
      rpg_operation.HandleOperation(self.game, option['operation'], option)
    
    
    # Select Dialogue
    if 'dialogue' in option and not payment_failed:
      self.SelectConversation(option['dialogue'])
      Log('Switch dialogue: %s' % option['dialogue'])
    
    
    # Add an achievement given by this option
    #NOTE(g): This is how stories are moved along, and quests can be successful.
    if 'achievement_add' in option and not payment_failed:
      #TODO(g): Wrap this into the player's object?
      self.player.achievements[option['achievement_add']] = True
      Log('Added achievement: %s' % option['achievement_add'])
    
    
    # Add a quest
    if 'quest_add' in option and not payment_failed:
      name = option['quest_add']
      
      if name in self.game.data['quests']:
        #TODO(g): deepcopy, so we can change the data freely
        self.player.quests[name] = self.game.data['quests'][name]
        Log('Added quest: %s' % name)
      else:
        Log('Quest not found: %s' % name, status=rpg_log.LEVEL_CRITICAL)
    
    
    # Refresh Options.  Things may have changed after this selection.
    self.GetOptions()

