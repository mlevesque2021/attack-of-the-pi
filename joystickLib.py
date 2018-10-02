#!/usr/bin/python
 
import spidev
import os
import time

# specifies the channel (pin) for the switch
swt_channel = 0

# specifies the channel for the Joystick x-axis
vrx_channel = 1

#specifies the channel for the Joystick y-axis
vry_channel = 2
 

delay = 0.5

# open a serial connection to the microprocessor
spi = spidev.SpiDev()
spi.open(0,0)
 
# function that recieves channel information and calls the spi.xfer function that returns an analog value on the specified channel
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data

# function that when called will produce a table that will show all x and y and button values
def debug():
  while True:
 
  
    vrx_pos = readChannel(vrx_channel)
    vry_pos = readChannel(vry_channel)
 
  
    swt_val = readChannel(swt_channel)
 
  
    print("VRx : {}  VRy : {}  SW : {}".format(vrx_pos,vry_pos,swt_val))
 
  
    time.sleep(delay)
