#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:54:30 2020
@author: Raymundo Cassani
"""

from keyboard_fusion_rgb import KeyboardFusionRGB
import time

keyboard = KeyboardFusionRGB(layout = 'eng_us')

# Set Static mode to Red
keyboard.set_static_mode(color_rgb=[0xff, 0x00, 0x00])
time.sleep(1)

# Set Flow mode
keyboard.set_flow_mode(speed=100, brightness=10)
time.sleep(2)
#keyboard.set_flow_mode(speed=100, brightness=100)
keyboard.set_brightness(80)
time.sleep(2)

# Set keyboard to Custom mode, and get current light configuration
dict_keys = keyboard.set_custom_mode(brightness = 100)

# Turn OFF all the keys (color RGB = [0x00, 0x00, 0x00])
for key in keyboard.keys:
  dict_keys[key] = [0x00, 0x00, 0x00]
keyboard.set_custom_configuration(dict_keys)

# Turn ON and OFF specific keys in the keyboard, with Blue light
characters = ['H', 'E', 'L', 'L', 'O', 'Space', 'W', 'O', 'R', 'L', 'D' ]
colors = [ [255, 0, 0], [255, 255, 0], [255, 0, 255], [0, 255, 0], [0, 255, 255],
           [0, 0, 255],
           [255, 255, 255], [255, 50, 150], [23, 147, 209], [0, 0, 255], [122, 30, 85]]
for character, color in zip(characters, colors):
  dict_keys[character] = color
  keyboard.set_custom_configuration(dict_keys)

# Layout for typing
l_pinky_keys =  ['1', '2', 'Q', 'A', 'Z', 'F1', 'F2']
l_pinky_color = [0, 255, 0]
r_pinky_keys =  ['0', '-', '=', 'P', '[', ']', ';', "'", '/', 'F10', 'F11', 'F12']
r_pinky_color = [0, 255, 0]
l_ring_keys =   ['3', 'W', 'S', 'X', 'F3']
l_ring_color =  [0, 255, 255]
r_ring_keys =   ['9', 'O', 'L', '.', 'F9']
r_ring_color =  [0, 255, 255]
l_middle_keys = ['4', 'E', 'D', 'C', 'F4']
l_middle_color= [255, 0, 255]
r_middle_keys = ['8', 'I', 'K', ',', 'F8']
r_middle_color =[255, 0, 255]
l_index_keys =  ['5', '6', 'R', 'T', 'F', 'G', 'V', 'B', 'F5', 'F6']
l_index_color = [255, 80, 0]
r_index_keys =  ['7', 'U', 'Y', 'J', 'H', 'M', 'N', 'F7']
r_index_color = [255, 160, 0]
thumb_keys =    ['Space']
thumb_color =   [0, 62, 255]
l_side_keys =   ['ESC', '~', 'Caps', 'Tab', 'Shift-L', 'Ctrl-L', 'WinKey', 'Fn', 'Alt-L']
l_side_color =  [0, 62, 255]
r_side_keys =   ['Pause', 'Del', 'Backspace', '\\', 'Enter', 'Ctrl-R', 'Shift-R', 'Menu', 'Alt-R']
r_side_color =  [0, 62, 255]
arrow_keys  =   ['Up', 'Down', 'Right', 'Left']
arrow_color =   [255, 0, 0]
numpad_keys =   ['NumLk', 'Num-.', 'Num-*', 'Num--', 'Num-/', 'Num-+', 'Num-Enter',
                 'Num-7', 'Num-4', 'Num-1', 'Num-8', 'Num-5', 'Num-2', 'Num-0', 'Num-9', 'Num-6', 'Num-3',]
numpad_color =  [160, 0, 255]
other_keys  =   ['Home', 'PgUp', 'PgDn', 'End']
other_color =   [255, 255, 255]

key_sets   = [l_pinky_keys, l_ring_keys, l_middle_keys, l_index_keys,
              r_pinky_keys, r_ring_keys, r_middle_keys, r_index_keys,
              thumb_keys, l_side_keys, r_side_keys, arrow_keys, numpad_keys, other_keys]
key_colors = [l_pinky_color, l_ring_color, l_middle_color, l_index_color,
              r_pinky_color, r_ring_color, r_middle_color, r_index_color,
              thumb_color, l_side_color, r_side_color, arrow_color, numpad_color, other_color]

# Set keyboard to Custom mode, and get current light configuration
dict_keys = keyboard.set_custom_mode(brightness = 100)

for key_set, key_color in zip(key_sets, key_colors):
  for key in key_set:
    dict_keys[key] = key_color

keyboard.set_custom_configuration(dict_keys)
keyboard.set_brightness(80)
