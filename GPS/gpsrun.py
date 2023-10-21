import time
from datetime import datetime
import board
import busio
import adafruit_gps
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import matplotlib.pyplot as plt

""""GPS Set-Up"""
i2c = board.I2C()
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)


"""GPS Config"""
gps.send_command(b"PMTK220,1000")
#sets the update rate to update GPS data every seccond
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
#sets the update info to GGA and RMC



while True:
    print(gps.update())
   