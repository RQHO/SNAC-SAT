import spidev
import RPi.GPIO as GPIO
import time
import os

class PowMan():

    #Open SPI bus
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=1000000
    
    # Function to read SPI data from MCP3008 chip
    # Channel must be an integer 0-7

    def ReadChannel(self):
        adc = self.spi.xfer2([1,(8+self.channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
    
    # Function to convert data to voltage level,
    # rounded to specified number of decimal places.
    def ConvertVolts(data,scale,places):
        #  volts = (data * 3.3) / float(1023)    #3.3V
        #  volts = (data * 5.0) / float(1023)     #for 5V with built in divider referenced to 3.3V
        volts = (data * scale) / float(1023)
        volts = round(volts,places)
        return volts

    # Define sensor channels

    # Prints voltage of 8 channels every second.
    # Author: Richard, edited by Quincy
    def getVolts(self):
        data_0 = self.ReadChannel(0)
        data_1 = self.ReadChannel(1)
    
        volts_0 = self.ConvertVolts(data_0, 5, 2)
        volts_1 = self.ConvertVolts(data_1, 5, 2)

        return((volts_0+volts_1)/2)
  
