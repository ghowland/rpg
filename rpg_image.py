#!/usr/bin/env python

"""
RPG: Image

Functions for dealing with images.
"""


import pygame
from pygame.locals import *
import pygame.surfarray
import os

import rpg_log as log


IMAGES = {}
FONTS = {}


# File to get our default font from
UI_DATA_FONT = 'data/ui/ui_font.txt'

# Default font if the data file doesnt exist
DEFAULT_FONT = 'data/fonts/tahoma.ttf'


def InitializeGraphics(core):
  pygame.init()
  
  # Create the core screen
  core.screen = pygame.display.set_mode(core.size)
  
  pygame.display.set_caption(core.title)
  
  #TODO(g): Always do this?
  pygame.mouse.set_visible(0)
  
  # Replace the default font with a specified one from a data file, if it exists
  if os.path.isfile(UI_DATA_FONT):
    log.Log('Testing UI Font data: %s' % UI_DATA_FONT)
    fontfile = open(UI_DATA_FONT).read().strip()
    log.Log('Testing UI Font file: %s' % fontfile)
    # If this is a real file, then set it as the new default
    if os.path.isfile(fontfile):
      global DEFAULT_FONT
      DEFAULT_FONT = fontfile
      log.Log('Swtiching default font: %s' % fontfile)

def Load(filename, colorkey=None, convert=True):
  global IMAGES
  
  if filename not in IMAGES:
    log.Log('Loading: %s' % filename)
    
    try:
      image = pygame.image.load(filename)
    except pygame.error, message:
      print 'Cannot load image:', filename
      raise SystemExit, message
    
    if convert:
      image = image.convert()
    
    if colorkey is not None:
      if colorkey is -1:
        colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey, RLEACCEL)
    
    IMAGES[filename] = image
  
  else:
    image = IMAGES[filename]
  
  return image


def GetFont():
  if pygame.font:
    font = pygame.font.Font(None, 36)
    return font
  else:
    return None


def GetPixel(image, pos):
  if 1:
    buffer = pygame.surfarray.pixels2d(image)
    
    try:
      pixel = buffer[pos[0]][pos[1]]
    except IndexError, e:
      #TODO(g): Error here?
      pixel = -1
  elif 0:
    buffer = image.get_buffer()
    
    width = image.get_width()
    height = image.get_height()
    bytesize = image.get_bytesize()
    runlength = width * bytesize
    
    pixel = buffer[(pos[1] * runlength) + (pos[0] * bytesize)]
  
  else:
    pixel = image.get_at(pos)
  
  return pixel


def GetImageBuffer(image):
  """Returns an array of the values for this image."""
  buffer = pygame.surfarray.pixels2d(image)
  
  return buffer




def DrawText(text, size, color, pos, surface, align_flag=0, outline=0,
             outline_color=0, width=-1, effect=0, effectPer=1.0, rectDim=None,
             font_filename=None):
  """Draw text of a given font size onto a surface"""
  # Initialize the offset
  offset = [0, 0]
  
  if font_filename == None:
    font_filename = DEFAULT_FONT
  
  # If there is no font system, return
  if not pygame.font:
    return offset
 
  # If there is no string, return
  if text == '':
    return offset
  
  # Initialize the font for sizes to be saved in it
  if font_filename not in FONTS:
    FONTS[font_filename] = {}
  
  # See if the font we need is in the dictionary
  if size not in FONTS[font_filename]:
    FONTS[font_filename][size] = pygame.font.Font(font_filename, size)
  
  font = FONTS[font_filename][size]
  
  # Determine the rect size.  May have been passed an argument, otherwise use the surface
  if rectDim is None:
    rectDim = (0, 0, surface.get_width(), surface.get_height())
  
  # Split the text into lines
  if text.find("\n", 0 ) != -1:
    lines = text.split("\n")
  else:
    lines = text.split("\\n")
  
  # Initialize counter
  count = 0
 
  # There is an effect
  if effect != 0:
    # If effect is vertical stretch
    if effect == 1:
      # If the percentage is over half
      if effectPer > 0.5:
        # Invert effect percentage, so it goes down again
        effectPer = 0.5 - (effectPer - 0.5)
      # Find scale
      scale = 1.0 + (0.17 * effectPer)
  
  # Loop through the lines
  for source_line in lines:
    # Check to see if this line is too long
    wrap_list = []	# Wrapped sentence list
    
    # If the width of this line is too big for our drawing width
    if font.size(source_line)[0] > rectDim[2]:
      # Split the line by spaces, and add a word each time checking if it is now too long
      words = source_line.split(' ')
      last_sentence = test_sentence = last_word = ''
      # Loop until we are out of words
      while len(words) > 0:
        last_sentence = test_sentence		# Save the last sentence
        last_word = words[0]				# Get the first word left in the list
        words.remove (last_word)			# Remove the word we just took from the list
        if test_sentence != '':
          test_sentence += " "			# Add space gap, if this isnt a fresh new sentence
        test_sentence += "%s" % last_word	# Add the word to the test sentence
        # If the test sentence is now too long
        if font.size(test_sentence)[0] > rectDim[2]:
          words.insert(0, last_word)		# Put the last word into the word list again, cause it's over the limit
          wrap_list.append(last_sentence)# Add the last sentence that was under the width to the wrapped sentence list
          last_sentence = test_sentence = last_word = ''
      # If the test sentence isnt blank, add it to the wrap list
      if test_sentence != '':
        wrap_list.append(test_sentence)
    # Else, it fits so just add the source line to our wrapped sentence list and move on
    else:
      wrap_list.append(source_line)
    
    # We now have a list of wrapped sentences.  Cycle through these to print them out
    for line in wrap_list:
      # If this isn't a blank line - No point in drawing blank lines
      if line != '':
        # If the text alignment should be centered
        if align_flag == 1:
          font_size = font.size(line)
          # If the width is not specified, use the Surface width
          if width == -1:
            offset[0] = (rectDim[2] / 2) - (font_size[0] / 2)
          # Else, use the specified width
          else:
            offset[0] = (width / 2) - (font_size[0] / 2)
        
        # If the text should be drawn with a black outline
        if outline == 1 or outline == 2:
          # Set data_flag_data to black value if not provided
          if outline_color == 0:
            outline_color = (0,0,0,255)
          
          # Render the font
          text_font = font.render(line, 1, outline_color)
          
          
          # If effect is vertical stretch
          if effect == 1:
            text_font = pygame.transform.scale(text_font, (text_font.get_width(), float(text_font.get_height()) * scale))
          
          
          # Blit the font - offset and line number adjusted
          if outline == 1 or outline == 2:
            surface.blit(text_font, (pos[0] + offset[0] + 1, pos[1] + offset[1] + 1 + (size * count * 1.2)))
          if outline == 2:
            surface.blit(text_font, (pos[0] + offset[0] + 2, pos[1] + offset[1] + 2 + (size * count * 1.2)))
          
        # Render the font
        text_font = font.render(line, 1, color)
        
        # If effect is vertical stretch
        if effect == 1:
          # If we havent already done this above in the flags
          if outline == 0:
            oldHeight = text_font.get_height()
            newHeight = text_font.get_height()
            offset[1] -= (newHeight-oldHeight) / 2
        
        # Blit the font - offset and line number adjusted - Also add the rectangle size we wanted to use for this writing (since we may want to draw in a portion of the surface, and treat it as a whole surface)
        surface.blit(text_font, (rectDim[0] + pos[0] + offset[0], rectDim[1] + pos[1] + offset[1] + (size * count * 1.2)))
        
      # Increment the counter
      count += 1
   
  # Return the offset and count information
  return (offset, count)
