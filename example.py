#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:54:30 2020

@author: cassani
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
  
