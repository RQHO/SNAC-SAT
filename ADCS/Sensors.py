import time
import numpy as np
import os
import board
import busio

from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lis3mdl import LIS3MDL

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = LSM6DSOX(i2c)
sensor2 = LIS3MDL(i2c)

def get_roll_am(accelX, accelY, accelZ):
    roll = (180 / np.pi) * np.arctan2(accelY, (np.sqrt(accelX ** 2 + accelZ ** 2)))
    return roll

def get_pitch_am(accelX, accelY, accelZ):
    pitch = (180 / np.pi) * np.arctan2(accelX, (np.sqrt(accelY ** 2 + accelZ ** 2)))
    return pitch

def get_yaw_am(accelX, accelY, accelZ, magX, magY, magZ):
    pitch = (180/np.pi) * np.arctan2(accelX, np.sqrt(accelY * accelY + accelZ * accelZ))
    roll = (180/np.pi) * np.arctan2(accelY, np.sqrt(accelX * accelX + accelZ * accelZ)) 

    mag_x = magX * np.cos(pitch) + magY * np.sin(roll) + magZ * np.cos(roll) * np.sin(pitch)
    mag_y = magY * np.cos(roll) - magY * np.sin(roll)
    
    yaw = (180/np.pi) * np.arctan2(-mag_y, mag_x)

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

    for i in range(50):
        magX, magY, magZ = sensor2.magnetic
        x = np.append(x, magX)
        y = np.append(y, magY)
        z = np.append(z, magZ)
        time.sleep(0.1)
    
    mag_offset = [np.mean(x), np.mean(y), np.mean(z)]

    print("Calibration complete.")
    return mag_offset

def calibrate_gyro():
    print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    time.sleep(3)
    print("Calibrating...")

    gyroX, gyroY, gyroZ = sensor1.gyro
    gyro_offset = [gyroX * (180/np.pi), gyroY * (180/np.pi), gyroZ * (180/np.pi)]

    print("Calibration complete.")
    return gyro_offset