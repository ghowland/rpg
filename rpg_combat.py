#!/usr/bin/env python

"""
RPG: Combat

When fighting, this class handles the logic.
"""


class Combatant:
  
  def __init__(self, actor):
    self.actor = actor
    
    # Make referencing the actor's data shorter
    self.data = actor.data
    
    # Action points remaining for this turn
    self.remaining_action_points = 0
    
    # Set this to the proper state in UpdateState, so we know how to act
    self.state = None
  
  
  def UpdateState(self):
    """Go through the actor's logic states, and set the current one."""


class Combat:
  
  def __init__(self, game, actors, map=None):
    self.game = game
    self.starting_actors = actors
    self.map = map
    
    # List of combatants, from enemy actors and playing characters
    self.combatants = []
    
    # This is just for handling input.  If true, we care about input states,
    #   if not we ignore them, because a battle is on and the player must
    #   wait their turn.
    self.players_turn = False
    
    # Add any combatants in the player's party
    #TODO(g): Get a list of the player's party
    self.AddCombatants([game.player])
    
    # Add any combatants from 
    self.AddCombatants(actors)
    
    # This is set in the future, and when time.time() passes it, the next
    #   update is allowed.  Used for delaying combat actions.
    self.next_update_time = None
    
    # This handles the Logic section for the combatants
    self.UpdateCombatantStates()
  
  
  def AddCombatants(self, actors):
    for actor in actors:
      self.combatants.append(Combatant(actor))
  
  
  
  def UpdateCombatantStates(self):
    """Go through all the combatants and update their states."""
    for combatant in self.combatants:
      combatant.UpdateState()
  
  
  def HandleInput(self, ticks=None):
    pass
