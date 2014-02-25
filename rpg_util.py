#!/usr/bin/env python

"""
RPG: Utility functions
"""


import StringIO


def YamlOpen(filename):
  data = open(filename).read()
  
  data = data.replace('\t', '  ')
  
  return StringIO.StringIO(data)
  
