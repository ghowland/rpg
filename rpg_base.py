#!/usr/bin/env python


import math


class Position:
  
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y


  def __repr__(self):
    output = '(%s, %s)' % (self.x, self.y)
    return output


  def IsSame(self, pos):
    if type(pos) in (tuple, list):
      if self.x == pos[0] and self.y == pos[1]:
        return True
      else:
        return False
    else:
      if self.x == pos.x and self.y == pos.y:
        return True
      else:
        return False


  def ToList(self):
    return [self.x, self.y]

  
  def Duplicate(self):
    return Position(self.x, self.y)


  def __getitem__(self, item):
    if item == 0:
      return self.x
    elif item == 1:
      return self.y
    else:
      raise IndexError('Position only has 0,1 indexes (x,y): %s' % item)


  def __setitem__(self, item, value):
    if item == 0:
      self.x = value
    elif item == 1:
      self.y = value
    else:
      raise IndexError('Position only has 0,1 indexes (x,y): %s' % item)


  def GetDistance(self, target):
    """Pythagorean theorum."""
    dx = abs(target[0] - self.x)
    dy = abs(target[1] - self.y)
    
    distance = math.sqrt(dx*dx + dy*dy)
    
    return distance


def GetLineBetweenPositions(source, target):
  """Get all the positional points between source and target."""
  source = list(source)
  target = list(target)
  
  points = []
  
  dx = float(target[0] - source[0])
  dy = float(target[1] - source[1])

  points.append(list(source))
  
  # If more horizontal
  if abs(dx) > abs(dy):
    slope = dy / dx
    b = source[1] - slope * source[0]
    
    if dx < 0:
      dx = -1
    else:
      dx = 1
    
    while source[0] != target[0]:
      source[0] += dx;
      y = int(slope * source[0] + b)
      points.append([source[0], y])
  
  # Else, more vertical
  else:
    slope = dx / dy
    b = source[0] - slope * source[1]
    
    if dy < 0:
      dy = -1
    else:
      dy = 1
    
    while source[1] != target[1]:
      source[1] += dy;
      x = int(slope * source[1] + b)
      points.append([x, source[1]])

  return points


def GetDistance(source, target):
  """Pythagorean theorum."""
  dx = abs(target[0] - source[0])
  dy = abs(target[1] - source[1])
  
  distance = math.sqrt(dx*dx + dy*dy)
  
  return distance


if __name__ == '__main__':
  # Test line drawing
  source = [5, 5]
  target = [10, 5] # Horizontal line
  #target = [0, 5] # Horizontal line: Reverse
  #target = [5, 0] # Vertical line
  #target = [5, 10] # Vertical line: Reverse
  #target = [10, 10] # Diagonal
  target = [0, 0] # Diagonal: Reverse
  #target = [7, 13] # Odd 1
  #target = [7, 17] # Odd 2
  target = [13, 7] # Odd 3
  target = [17, 7] # Odd 4
  
  source = [42 ,17]
  target = [44, 24]
  
  if 1:
    points = GetLineBetweenPositions(source, target)
    print points
  elif 1:
    print '%s -> %s' % (source, target)
    print GetDistance(source, target)
  
