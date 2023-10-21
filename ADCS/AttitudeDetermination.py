from Sensors import *

import time
import numpy as np
import os
import board
import busio
import sys
import math

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lis3mdl import LIS3MDL



class orient:

    i2c = busio.I2C(board.SCL, board.SDA)
    #accelerometer and gyro
    sensor1 = LSM6DSOX(i2c)
    #magnetometer
    sensor2 = LIS3MDL(i2c)

    def get_roll_am(accelX, accelY, accelZ):
        roll = (180 / np.pi) * np.arctan(accelY / accelZ)
        return roll

    def get_pitch_am(accelX, accelY, accelZ):
        pitch = (180 / np.pi) * np.arctan(-accelX/ np.sqrt(accelY ** 2 + accelZ ** 2))
        return pitch

    def get_yaw_am(accelX, accelY, accelZ, magX, magY, magZ):
        roll = get_roll_am(accelX, accelY, accelZ)
        pitch = get_pitch_am(accelX, accelY, accelZ)

        mag_x = magX * np.cos(pitch) + magY * np.sin(roll) + magZ * np.cos(roll) * np.sin(pitch)
        mag_y = magY * np.cos(roll) - magY * np.sin(roll)
        yaw = (180/np.pi) * np.arctan(-mag_y / mag_x)
        return yaw

    def get_roll_gy(prev_angle, delT, gyro):
        roll = prev_angle[0] + gyro[0] * delT
        return roll
    
    def get_pitch_gy(prev_angle, delT, gyro):
        pitch = prev_angle[1] + gyro[1] * delT
        return pitch
    
    def get_yaw_gy(prev_angle, delT, gyro):
        yaw = prev_angle[2] + gyro[2] * delT
        return yaw

    def set_initial(mag_offset = [0, 0, 0]):
        # Sets the initial position for plotting and gyro calculations.
        print("Preparing to set initial angle. Please hold the IMU still.")
        time.sleep(5)
        print("Setting angle...")

        accelX, accelY, accelZ = sensor1.acceleration #m/s^2
        magX, magY, magZ = sensor2.magnetic #gauss

        # Calibrate magnetometer readings.
        magX = magX - mag_offset[0]
        magY = magY - mag_offset[1]
        magZ = magZ - mag_offset[2]

        roll = get_roll_am(accelX, accelY,accelZ)
        pitch = get_pitch_am(accelX, accelY, accelZ)
        yaw = get_yaw_am(accelX, accelY, accelZ, magX, magY, magZ)

        print("Initial angle set.")

        return [roll, pitch, yaw]

    @staticmethod
    def isTurningGy(gyro_offset):
        while True:
            gyroX, gyroY, gyroZ = sensor1.gyro

            gyroX = gyroX - gyro_offset[0]
            gyroY = gyroY - gyro_offset[0]
            gyroZ = gyroZ - gyro_offset[0]

            #print(gyroZ)
            if abs(gyroZ) > 1.2:
                return True
    @staticmethod
    def calibrate_mag():
        # TODO: Set up lists, time, etc
        print("Preparing to calibrate magnetometer. Please wave around.")
        time.sleep(3)
        print("Calibrating...")

        # TODO: Calculate calibration constants. Remember: the idea is to
        # collect a lot of test points, average them, and use those as offsets
        x = np.array([])
        y = np.array([])
        z = np.array([])

        for i in range(100):
            magX, magY, magZ = sensor2.magnetic
            x = np.append(x, magX)
            y = np.append(y, magY)
            z = np.append(z, magZ)
            time.sleep(0.1)
        
        mag_offset = [np.mean(x), np.mean(y), np.mean(z)]

        print("Calibration complete.")
        return mag_offset
    @staticmethod
    def calibrate_gyro():
        print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
        time.sleep(5)
        print("Calibrating...")

        gyroX, gyroY, gyroZ = sensor1.gyro
        #gyro_offset = [gyroX * (180/np.pi), gyroY * (180/np.pi), gyroZ * (180/np.pi)]
        gyro_offset = [gyroX, gyroY, gyroZ]

        print("Calibration complete.")
        return gyro_offset

    # Report angle and position
    @staticmethod
    def turnCheck(offset1):
        """
        Prints the roll, pitch, and yaw angles, and the x, y, and z positions.
        """
        mag_offset = offset1
        previous_yaw = 0

        position_x = 0
        position_y = 0

        dt = 1

        while True:
            accelX, accelY, accelZ = sensor1.acceleration
            magX, magY, magZ = sensor2.magnetic

            magX = magX - mag_offset[0]
            magY = magY - mag_offset[1]
            magZ = magZ - mag_offset[2]

            roll_am = get_roll_am(accelX, accelY, accelZ)
            pitch_am = get_pitch_am(accelX, accelY, accelZ)
            yaw_am = get_yaw_am(accelX, accelY, accelZ, magX, magY, magZ)
            
            position_x += 0.5 * accelX * dt ** 2
            position_y += 0.5 * accelY * dt ** 2

            #print("Accelerometer and Magnetometer:")
            print(f"Yaw: {round(yaw_am, 2)}")
            print(f"X: {round(position_x, 1)}, Y: {round(position_y, 1)}")
            if previous_yaw == 0:
                previous_yaw = yaw_am
            
            if abs(abs(yaw_am) - abs(previous_yaw)) > 45:
                print("Roter")
                return True
            #else:
                #print("No yaw detected")

            previous_yaw = yaw_am

            time.sleep(dt)
