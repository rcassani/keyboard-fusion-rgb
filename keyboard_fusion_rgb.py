#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Driver for lights of Fusion RGB Keyboard in AORUS 15G

Keyboard description:
  
VENDOR ID  = 0x1044
PRODUCT id = 0x7A3C
Chu Yuen Enterprise Co., Ltd Fusion RGB KB

@author: Raymundo Cassani
"""
import hid
import time
import numpy as np

class KeyboardFusionRGB:
  """
  Class to control the RGB lights of the AOURS Fusion RGB Keyboard
  VENDOR ID  = 0x1044, PRODUCT id = 0x7A3C, Chu Yuen Enterprise Co., Ltd 
  """

  def __init__(self, layout = 'eng_us'):
    
    self.vendor_id = 0x1044
    self.product_id = 0x7A3C
     
    self.delay_s = 0.01     # delay in seconds
    self.data_size = 264    # number of bytes of the feature report
    self.n_keys = 128       # number of keys for the custom lights
    
    # Modes   
    # Code, Name,           Method
    # 0x00, Static,         set_static_mode()
    # 0x01, Breathing,      set_breathing_mode()
    # 0x02, Flow,           set_flow_mode() 
    # 0x03, Firework,       set_firework_mode()  
    # 0x04, Ripple,         set_ripple_mode() 
    # 0x05, Rain,           set_rain_mode() 
    # 0x06, Cycling,        set_cycling_mode() 
    # 0x07, Trigger,        set_trigger_mode() 
    # 0x08, Pulse,          set_pulse_mode() 
    # 0x09, Radar,          set_radar_mode() 
    # 0x0A, Star Shinning,  set_star_mode() 
    # 0x0B, Wave,           set_wave_mode() 
    # 0x0C, Cross,          set_cross_mode() 
    # 0x0D, Dragonstrike,   set_dragonstrike_mode() 
    # 0x0E, Bloom,          set_bloom_mode() 
    # 0x0F, Spiral,         set_spiral_mode() 
    # 0x10, Merge,          set_merge_mode() 
    # 0x11, Crash,          set_crash_mode() 
    # 0x12, Custom,         set_custom_mode() 

    self.mode_offsets = {0x00:0, 0x01:4, 0x02:9, 0x03:11, 0x04:16, 0x05:21, 
                         0x06:26, 0x07:27, 0x08:32, 0x09:37, 0x0A:43, 
                         0x0B:48, 0x0C:54, 0x0D:59, 0x0E:68, 0x0F:76,
                         0x10:78, 0x11:86, 0x12:0}

    # Key order for the ENG-US keyboard, only 101 keys are used
    # the key order may change for other keyboard layouts    
    eng_us_keys = ['N/A', 'N/A', 'N/A', 'N/A', 'Ctrl-R', 'PgUp', 'Ctrl-L', 'F5',
                   'Q', 'Tab', 'A', 'ESC', 'Z', 'N/A', '~', '1', 
                   'W', 'Caps', 'S', 'N/A', 'X', 'N/A', 'F1', '2',
                   'E', 'F3', 'D', 'F4', 'C', 'N/A', 'F2', '3',
                   'R', 'T', 'F', 'G', 'V', 'B', '5', '4',
                   'U', 'Y', 'J', 'H', 'M', 'N', '6', '7', 
                   'I', ']', 'K', 'F6', ',', 'N/A', '=', '8',
                   'O', 'F7', 'L', 'N/A', '.', 'Menu', 'F8', '9', 
                   'P', '[', ';', "'", 'N/A', '/', '-', '0',
                   'N/A', 'N/A', 'N/A', 'Alt-L', 'N/A', 'Alt-R', 'N/A', 'Pause',
                   'N/A', 'Backspace', '\\', 'F11', 'Enter', 'F12', 'F9', 'F10',
                   'Num-7', 'Num-4', 'Num-1', 'Space', 'NumLk', 'Down', 'Home', 'N/A', 
                   'Num-8', 'Num-5', 'Num-2', 'Num-0', 'Num-/', 'Right', 'N/A', 'Del', 
                   'Num-9', 'Num-6', 'Num-3', 'Num-.', 'Num-*', 'Num--', 'N/A', 'PgDn',
                   'Num-+', 'N/A', 'Num-Enter', 'Up', 'N/A', 'Left', 'N/A', 'End',
                   'N/A', 'Shift-L', 'Shift-R', 'N/A', 'WinKey', 'Fn', 'N/A', 'N/A']

    
    #for now only ENG-US layout is supported     
    if layout == 'eng_us':
      self.keys = eng_us_keys
    else:
      self.keys = eng_us_keys 
    
    # empty HID device
    self.hid_kb = hid.device()  


  def open_hid_comm(self):
    '''
    Opens the communication with the HID keyboard and checks for errors
    '''
    
    try:
      self.handle = self.hid_kb.open(self.vendor_id, self.product_id)
    except:
      print("Could not open HID keyboard") 
  
  
  def close_hid_comm(self):
    '''
    Closes the communication with the HID keyboard    
    '''
    
    self.hid_kb.close()
    
    
  def write_keyboard_request(self, buf_req, has_rsp=False):
    '''
    Writes a request to the HID keyboard and reads the response if indicated

    Parameters
    ----------
    buf_req : List of Int (8-bits)
      DESCRIPTION. Request to write to the HID keyboard
    has_rsp : Boolean, optional
      DESCRIPTION. Indicates if a response is expected for the given request

    Returns
    -------
    buf_rsp : List of integers (16 bits) 
      DESCRIPTION. Response of the HID keyboard, or None if has_rsp == False 
    '''
    
    self.open_hid_comm()
    # send request
    try:
      self.hid_kb.send_feature_report(buf_req)
      time.sleep(self.delay_s)
    except:
      print('Error at send_feature_report()')
      self.close_hid_comm()
      return None
    # read if there is response
    if has_rsp:
      try:
        buf_rsp = self.hid_kb.get_feature_report(self.data_size, self.data_size)
        time.sleep(self.delay_s)
        self.close_hid_comm()
        return buf_rsp
      except:
        print('Error at get_feature_report()')
        self.close_hid_comm()
        return None
    else:
      self.close_hid_comm()
      return None
        
  def set_mode_configuration(self, mode, brightness, buf_mode):
    '''
    Sets a mode with its configuration

    Parameters
    ----------
    mode : Int (8-bit)
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100
    buf_mode : List Int (8-bit)
      DESCRIPTION. Specific configuration for the indicated mode
    '''
    
    offset = self.mode_offsets[mode]
    buf_req = ([0x07, 0x02] + [0x00] * 8 + # instructions to set mode
               [mode]                    + # mode code
               [0x00]                    + # seems useless
               [brightness]              + # brightness
               [0x00] * offset           + # offset        
               buf_mode)                   # configuration buffer for mode    
    n_fill = self.data_size - len(buf_req)
    buf_req = buf_req + [0x00] * n_fill    # fill up to 264 bytes
    self.write_keyboard_request(buf_req)

      
  def get_current_status(self):
    '''
    Gets the current configuration of the HID keyboard

    Returns
    -------
    buf_rsp : List of integers (16 bits) 
      DESCRIPTION. Current configuration of the HID keyboard
    '''
    
    buf_req = [0x07, 0x82] + [0x00] * 262
    buf_rsp = self.write_keyboard_request(buf_req, has_rsp=True)
    return buf_rsp 
    
  
  def clean_configuration(self):
    '''
    Write the cleaning configuration command and check for error
    '''
    
    buf_req = [0x07, 0x8A] + [0x00] * 262
    buf_rsp = self.write_keyboard_request(buf_req, has_rsp=True)
    # check the the response for cleaning is full of 0x00
    buf_rsp.pop(0) # except the first byte
    if not all(element == 0x00 for element in buf_rsp):
      print('Error at Response for Cleaning command')  
  
  def set_brightness(self, brightness):
    buf_req = self.get_current_status()
    buf_req[1] = 0x02         # change instruction
    buf_req[12] = brightness  # change brightness
    self.write_keyboard_request(buf_req)
  
  
  # MODES 0x00 to 0x11  
  def set_static_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], brightness = 50):
    '''
    Sets the keyboard lights to Static mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50
    '''
    
    self.clean_configuration()
    buf_mode = [0x00] + color_rgb
    self.set_mode_configuration(0x00, brightness, buf_mode)

    
  def set_breathing_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Breathing mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed] + [0x00] + color_rgb
    self.set_mode_configuration(0x01, brightness, buf_mode)
    
  def set_flow_mode(self, speed = 50, direction = 'right', brightness = 50):
    '''
    Sets the keyboard lights to Flow mode

    Parameters
    ----------
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Flow direction, values: "right" (default), "left", "up" and "down"
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'right':
      dir_mode = 0
    elif direction == 'left':
      dir_mode = 1
    elif direction == 'down':
      dir_mode = 2
    elif direction == 'up':
      dir_mode = 3
    else:
      dir_mode = 0  
    buf_mode = [speed, dir_mode]  
    self.set_mode_configuration(0x02, brightness, buf_mode)
   
  def set_firework_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Firework mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x03, brightness, buf_mode)

  def set_ripple_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Ripple mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
 
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, 0x02] + color_rgb
    self.set_mode_configuration(0x04, brightness, buf_mode)
    
  def set_rain_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Rain mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''

    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x05, brightness, buf_mode)

  def set_cycling_mode(self, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Cycling mode

    Parameters
    ----------
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed]
    self.set_mode_configuration(0x06, brightness, buf_mode)
    
  def set_trigger_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Trigger mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x07, brightness, buf_mode)
    
  def set_pulse_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Pulse mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x08, brightness, buf_mode)

  def set_radar_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, direction = 'cw', brightness = 50):
    '''
    Sets the keyboard lights to Radar mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Radar direction, "cw" = clockwise (default), "ccw" = counter clockwise
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'cw':
      dir_mode = 1
    elif direction == 'ccw':
      dir_mode = 0
    else:
      dir_mode = 1  
    buf_mode = [speed, int(random), dir_mode] + color_rgb
    self.set_mode_configuration(0x09, brightness, buf_mode)

  def set_star_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Star shining mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''

    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x0A, brightness, buf_mode)

  def set_wave_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, direction = 'right', brightness = 50):
    '''
    Sets the keyboard lights to Wave mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Wave direction, values: "right" (default), "left", "up" and "down"
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'right':
      dir_mode = 0
    elif direction == 'left':
      dir_mode = 1
    elif direction == 'up':
      dir_mode = 2
    elif direction == 'down':
      dir_mode = 3
    else:
      dir_mode = 0  
    buf_mode = [speed, int(random), dir_mode] + color_rgb
    self.set_mode_configuration(0x0B, brightness, buf_mode)

  def set_cross_mode(self, color_rgb = [0xFF, 0xFF, 0xFF], random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Cross mode

    Parameters
    ----------
    color_rgb : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0xFF, 0xFF]
    random : Boolean
      DESCRIPTION. The color in randomly selected, color_rgb is ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb
    self.set_mode_configuration(0x0C, brightness, buf_mode)

  def set_dragonstrike_mode(self, color_rgb_1 = [0xFF, 0x00, 0x00], color_rgb_2 = [0x00, 0x00, 0xFF],
                            random = False, speed = 50, direction = 'right', brightness = 50):
    '''
    Sets the keyboard lights to Dragonstrike mode

    Parameters
    ----------
    color_rgb_1 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0x00, 0x00]
    color_rgb_2 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0x00, 0x00, 0xFF]
    random : Boolean
      DESCRIPTION. The colors are randomly selected, color_rgb_1 and color_rgb_2 are ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Dragonstrike direction, values: "right" (default), "left", "up" and "down"
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'right':
      dir_mode = 0
    elif direction == 'left':
      dir_mode = 1
    else:
      dir_mode = 0  
    buf_mode = [speed, int(random), dir_mode] + color_rgb_1 + color_rgb_2
    self.set_mode_configuration(0x0D, brightness, buf_mode)

  def set_bloom_mode(self, color_rgb_1 = [0xFF, 0x00, 0x00], color_rgb_2 = [0x00, 0x00, 0xFF],
                            random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Bloom mode

    Parameters
    ----------
    color_rgb_1 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0x00, 0x00]
    color_rgb_2 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0x00, 0x00, 0xFF]
    random : Boolean
      DESCRIPTION. The colors are randomly selected, color_rgb_1 and color_rgb_2 are ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb_1 + color_rgb_2
    self.set_mode_configuration(0x0E, brightness, buf_mode)

  def set_spiral_mode(self, speed = 50, direction = 'cw', brightness = 50):
    '''
    Sets the keyboard lights to Spiral mode, color are random

    Parameters
    ----------
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Spiral direction, values: "cw" = clockwise (default), "ccw" = counter clockwise
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'cw':
      dir_mode = 0
    elif direction == 'ccw':
      dir_mode = 1
    else:
      dir_mode = 0   
    buf_mode = [dir_mode, speed]  
    self.set_mode_configuration(0x0F, brightness, buf_mode)

  def set_merge_mode(self, color_rgb_1 = [0xFF, 0x00, 0x00], color_rgb_2 = [0x00, 0x00, 0xFF],
                            random = False, speed = 50, brightness = 50):
    '''
    Sets the keyboard lights to Merge mode

    Parameters
    ----------
    color_rgb_1 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0x00, 0x00]
    color_rgb_2 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0x00, 0x00, 0xFF]
    random : Boolean
      DESCRIPTION. The colors are randomly selected, color_rgb_1 and color_rgb_2 are ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    buf_mode = [speed, int(random)] + color_rgb_1 + color_rgb_2
    self.set_mode_configuration(0x10, brightness, buf_mode)

  def set_crash_mode(self, color_rgb_1 = [0xFF, 0x00, 0x00], color_rgb_2 = [0x00, 0x00, 0xFF],
                            random = False, speed = 50, direction = 'horizontal', brightness = 50):
    '''
    Sets the keyboard lights to Crash mode

    Parameters
    ----------
    color_rgb_1 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0xFF, 0x00, 0x00]
    color_rgb_2 : List 3 Int (8-bit) RGB
      DESCRIPTION. RGB color 0 to 255, the default is [0x00, 0x00, 0xFF]
    random : Boolean
      DESCRIPTION. The colors are randomly selected, color_rgb_1 and color_rgb_2 are ignored
    speed : Int (8-bit), optional
      DESCRIPTION. Speed values 0 to 100 The default is 50.
    direction: String, optional
      DESCRIPTION. Crash direction, values: "horizontal" (default) and "vertical"
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 
    '''
    
    self.clean_configuration()
    speed = 10 - round(speed / 10)
    if direction == 'horizontal':
      dir_mode = 0
    elif direction == 'vertical':
      dir_mode = 1
    else:
      dir_mode = 0  
    buf_mode = [speed, int(random), dir_mode] + color_rgb_1 + color_rgb_2
    self.set_mode_configuration(0x11, brightness, buf_mode)
  
  # Custom mode 0x12
  def set_custom_mode(self, dict_keys = [], brightness = 50):
    '''
    Sets the light configuration for the Custom mode.
    If dict_keys is provided:
      The Custom mde is set and updated to the values in dict_keys
    If dict_keys is not provided, 
      The Custom mode is set, and the stored value is retrieved and returned

    Parameters
    ----------
    dict_keys : Dictionary, optional
      DESCRIPTION. Dictionary for the color RGB for each key, the default is [].
    brightness : Int (8-bit), optional
      DESCRIPTION. Brightness level 0 to 100, the default is 50 

    Returns
    -------
    dict_keys : Dictionary
      DESCRIPTION. Dictionary for the color RGB for each key
    '''
    
    self.clean_configuration()
    self.set_mode_configuration(0x12, brightness, [])
    if dict_keys:
      # write new configuration
      self.set_custom_configuration(dict_keys)
    # read current configuration
    dict_keys = self.get_custom_configuration() 
    return dict_keys
     
  def get_custom_configuration(self):
    '''
    Gets the stored light values in the Custom mode

    Returns
    -------
    dict_keys : Dictionary
      DESCRIPTION. Dictionary for the color RGB for each key
    '''
    
    buf_req = [0x07, 0x86, 0x00, 0x01] + [0x00] * 260
    buf_rsp_1 = self.write_keyboard_request(buf_req, has_rsp=True)
    buf_req = [0x07, 0x86, 0x00, 0x02] + [0x00] * 260
    buf_rsp_2 = self.write_keyboard_request(buf_req, has_rsp=True)
    buf_rsp = buf_rsp_1[8:] + buf_rsp_2[8:] 
    # convert these buffers to dictionary
    tmp = np.array(buf_rsp[:384]) # 128 keys times 3 bytes for color (RGB)
    hex_rgb = np.reshape(tmp, (128,3), order='F') 
    dict_keys = {}
    for ix_key in range(128):
      dict_keys[self.keys[ix_key]] = list(hex_rgb[ix_key, :]) 
    return dict_keys

  def set_custom_configuration(self, dict_keys):
    '''
    Sets the stored light values in the Custom mode

    Parameters
    ----------
    dict_keys : Dictionary
      DESCRIPTION. Dictionary for the color RGB for each key
    '''
    
    # dictionary to buffers
    hex_rgb = np.zeros((128, 3), int)
    for ix_key in range(128):
      hex_rgb[ix_key, :] = np.array(dict_keys[self.keys[ix_key]])
    tmp = list(np.reshape(hex_rgb, 384, 'F'))
    msg_1 = tmp[:256] # Red and Green
    msg_2 = tmp[256:] # Blue
    buf_req_1 = [0x07, 0x06, 0x00, 0x01] + [0x00] * 4 + msg_1
    buf_req_2 = [0x07, 0x06, 0x00, 0x02] + [0x00] * 4 + msg_2 + [0x00]*128
    self.write_keyboard_request(buf_req_1)
    self.write_keyboard_request(buf_req_2)
     
