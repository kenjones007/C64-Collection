#!/usr/bin/env python3
# ===================================================================================
# Project:   TapeBuddy64 - Python Script for Command Line Interface - Flash Firmware
# Version:   v1.1
# Year:      2021
# Author:    Stefan Wagner
# Github:    https://github.com/wagiminator
# License:   http://creativecommons.org/licenses/by-sa/3.0/
# ===================================================================================
#
# Description:
# ------------
# Flashes firmware for the TapeBuddy64 adapter.
#
# Dependencies:
# -------------
# - tinyupdi (included in libs folder)
#
# Operating Instructions:
# -----------------------
# - Set the serial mode switch on your TapeBuddy64 adapter to "UPDI"
# - Connect the adapter to a USB port of your PC
# - Execute this skript: python flash-firmware.py


import sys
from libs.tinyupdi import Programmer, PrgError


# Valid target MCUs
FIRMWARE_TARGETS = {
    0x1E9226: 'attiny404',
    0x1E9222: 'attiny414',
    0x1E9325: 'attiny804',
    0x1E9322: 'attiny814',
    0x1E9425: 'attiny1604',
    0x1E9422: 'attiny1614'  }

# Fuse settings
FIRMWARE_FUSES = {0:0x00, 1:0x00, 2:0x01, 4:0x00, 5:0xC5, 6:0x04, 7:0x00, 8:0x00}

# Binary file
FIRMWARE_BIN = 'libs/firmware.bin'


# Print Header
print('')
print('--------------------------------------------------')
print('TapeBuddy64 - Python Command Line Interface v1.1')
print('(C) 2022 by Stefan Wagner - github.com/wagiminator')
print('--------------------------------------------------')


# Establish serial connection
print('Connecting to device ...')
tinyupdi = Programmer()
if not tinyupdi.is_open:
    print('Check if serial mode switch is set to "UPDI"')
    raise PrgError('Device not found')


# Enter progmode
print('Entering programming mode ...')
try:
    tinyupdi.enter_progmode()
except:
    print('Device is locked, performing unlock with chip erase')
    tinyupdi.unlock()


# Read device ID, identify target MCU
print('Pinging target MCU ...')
devid = tinyupdi.get_device_id()
if devid in FIRMWARE_TARGETS:
    print('Target device found:', FIRMWARE_TARGETS[devid])
else:
    tinyupdi.leave_progmode()
    tinyupdi.close()
    raise PrgError('Unknown or unsupported target device')


# Flash firmware
if not tinyupdi.flash_bin(FIRMWARE_BIN):
    tinyupdi.leave_progmode()
    tinyupdi.close()
    raise PrgError('Failed to flash firmware')


# Burning fuses
print('Writing and verifying fuses ...')
for f in FIRMWARE_FUSES:
    if not tinyupdi.set_fuse(f, FIRMWARE_FUSES[f]):
        tinyupdi.leave_progmode()
        tinyupdi.close()
        raise PrgError('Failed to burn fuses')


# Finish all up
tinyupdi.leave_progmode()
tinyupdi.close()
print('Done.')
print('Set serial mode switch back to "UART"')
print('')