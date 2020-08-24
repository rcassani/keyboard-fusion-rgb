# Keyboard Fusion RGB
Python driver to control the lights in the keyboard in laptop AOURUS 15G.

Keyboad information
```
idVendor      : 0x1044 Chu Yuen Enterprise Co., Ltd
idProduct     : 0x7a3c
iManufacturer : GIGABYTE
iProduct      : Fusion RGB KB  
```
<center>
<img src="https://user-images.githubusercontent.com/8238803/91067085-78d78480-e600-11ea-8f1c-b879a2a7a8d7.png" style="width:40%">
<img src="https://user-images.githubusercontent.com/8238803/91067102-80972900-e600-11ea-993d-059be89ce2dc.png" style="width:40%">
</center>

This dirver was developed by reverse engineering the communication protocol between the Fusion RGB keyboard and the AOURS Control Center application (for Windows). Each key in the keyboard has a RGB LED that can be controlled individually. The keyboard can be set to any of the 17 [pre-programmed modes]() or to a [Custom mode]() where the static color of key is configured separately. In Custom mode, for the moment only the [ENG-US]() layout is supported.

The communication protocol was implemented with the [HIDAPI library](https://github.com/libusb/hidapi), more specifically with [cython-hidapi](https://github.com/trezor/cython-hidapi), which is a Python wrapper for the HIDAPI library.

# Dependencies
* [cython-hidapi](https://github.com/trezor/cython-hidapi)
  `# pip install hidapi`

* [HIDAPI library](https://github.com/libusb/hidapi)    
  ` # pacman -S hidapi`   for Arch Linux  
  ` # yum install hidapi` for CentOS / RHEL  
  ` # dnf install hidapi` for Fedora  
  ` # apt install libhidapi-hidraw0` for Mint / Ubuntu / Debian

# Installation
* Clone repo  
  `$ git clone https://github.com/rcassani/keyboard-fusion-rgb.git`

* Install Python module
  `$ cd keyboard-fusion-rgb`
  `$ pip install .`

# Permissions
The driver needs write permissions over the keyboard. This can be run by running as root (not recommened) or modifying the permissions for the keyboard with one of the following two methods:

1. **Temporal**: This process has to be done everytimne the keyboard is "disconnected".

  * Identify the Bus and Device for the keyboard:
  `$ lsusb`  
  `Bus 001 Device 006: ID 1044:7a3c Chu Yuen Enterprise Co., Ltd Fusion RGB KB`

  * Change the permissions on the device
  `chmod -R 666  /dev/bus/usb/001/004`

2. **Permanent**: A (`udev`)[] rule is create to change the permissions over the keyboard everytimne it is "connected".

  * Make the u`dev` rule: create the file `/etc/udev/rules.d/50-keyboard-fusion-rgb.rules` with the following content:
  `SUBSYSTEM=="usb", ATTRS{idVendor}=="1044", ATTR{idProduct}=="7a3c", MODE="0666"`

  * Reload the `udev` rules:
  `# udevadm control --reload-rules && udevadm trigger`

# Usage
This snippet shows how to set the all keyboard lights to red.
```
from keyboard_fusion_rgb import KeyboardFusionRGB

keyboard = KeyboardFusionRGB(layout = 'eng_us')
keyboard.set_static_mode(color_rgb=[0xff, 0x00, 0x00])
```
# Methods
## Pre-programmed Modes
The keyboad can be set to any of the 17 pre-programmed modes.
Each mode can configured in brigness. Some modes have extra features such as speed, direction, and random color. See the description of each method to see what parameters apply.

| Code  | Name          | Method                  |
|----------|----------------|-------------------------|
|     0x00 | Static        | set_static_mode()       |
|     0x01 | Breathing     | set_breathing_mode()    |
|     0x02 | Flow          | set_flow_mode()         |
|     0x03 | Firework      | set_firework_mode()     |
|     0x04 | Ripple        | set_ripple_mode()       |
|     0x05 | Rain          | set_rain_mode()         |
|     0x06 | Cycling       | set_cycling_mode()      |
|     0x07 | Trigger       | set_trigger_mode()      |
|     0x08 | Pulse         | set_pulse_mode()        |
|     0x09 | Radar         | set_radar_mode()        |
|     0x0A | Star Shinning | set_star_mode()         |
|     0x0B | Wave          | set_wave_mode()         |
|     0x0C | Cross         | set_cross_mode()        |
|     0x0D | Dragonstrike  | set_dragonstrike_mode() |
|     0x0E | Bloom         | set_bloom_mode()        |
|     0x0F | Spiral        | set_spiral_mode()       |
|     0x10 | Merge         | set_merge_mode()        |
|     0x11 | Crash         | set_crash_mode()        |

## Custom mode
In custom mode, the color for each key is selected individually. To do this a dictionary with the keys and colors is created:
```
# Set keyboard to Custom mode (0x12), and get current light configuration
dict_keys = keyboard.set_custom_mode()
# Color for letter A is updated to Blue
dict_keys['A'] = [0x00, 0x00, 0xFF]
# Updates the Custom mode to the new dictionary
keyboard.set_custom_configuration(dict_keys)
```

# Protocol
The request messages (REQ) from the PC to the keyboard, have a lenght of 300 bytes; and the response (RSP) messages have a lenght of 292. Althoug for both cases only the last 264 bytes are the instructions the data that is used to configure the keyboard.

A full description of the REQ and RSP messages can be found in this [spreeadsheet](https://docs.google.com/spreadsheets/d/1ypcfDOhsm0H5z6wsgtpZg-oJ0oQ4zxjGwoJ37xBPDqA/edit?usp=sharing).
