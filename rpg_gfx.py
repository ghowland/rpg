#!/usr/bin/env python


import pygame


def Draw(source, target, pos):
  """Draw the source image onto the target at pos position."""
  target.blit(source, pos)


def DrawBlack(target, pos, size):
  """Draw a black rectangle."""
  target.fill((0,0,0), (pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]))


