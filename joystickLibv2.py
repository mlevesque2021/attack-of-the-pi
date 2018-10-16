#!/usr/bin/python
 
import spidev
import os
import time

DEBUG = False

# define mcp channels
swt_channel = 0
vrx_channel = 1
 
# delay in between data reads
delay = 0.1

# open a serial connection to the mcp
spi = spidev.SpiDev()
spi.open(0,0)
 
# function that recieves channel number and ouputs Joystick Pos and Button Status
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  mStatus = ""
  fStatus = "NO"
  if channel == 1:
    if data in range(500, 580):
      mStatus = "False"
    elif data < 500:
      mStatus = "Left"
    else:
      mStatus = "Right"
  elif channel == 0:
    if data == 1023:
      fStatus = "YES"
    return fStatus
  return mStatus


# A debugging tool that when enabled will ouput joystick and button status along with the analog vvalue for each
while DEBUG:
 
  
  mStatus = readChannel(vrx_channel)
 
  
  fStatus = readChannel(swt_channel)
 
  
  print("VRx :   Direction? : {}  Fire? : {}".format(mStatus, fStatus))
 
  
  time.sleep(delay)
