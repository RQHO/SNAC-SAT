import os
import sys
import time
import queue
import board
import busio
CorePath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

sys.path.insert(0,CorePath+"/ADCS/")
sys.path.insert(0,CorePath+"/Imaging/")
sys.path.insert(0,CorePath+"/Comms/")
sys.path.insert(0,CorePath+"/Power/")

print(CorePath)
from send import CommSend
from TakePic import pictake 
import threading
from AttitudeDetermination import orient
from FileProcessing import fproc
from power import PowMan

from picamera2 import Picamera2
import adafruit_gps
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX





'''assuming the following:
leg 0 = not defined
leg 1 = imaging 1
leg 2 = imaging 2
leg 3 = charging
leg 4 = transmitting
'''
legPos = 1
#from picamera2 import Picamera2


pictures = pictake()

ADCS = orient()
Comms = CommSend()
powerMan = PowMan()

sharedQueue = queue.Queue()
timeQueue = queue.Queue()
lock = threading.Lock()

def LegRun():#hehehe legs run
    gyr_offset = ADCS.calibrate_gyro()
    holdPos = 0
    while True:
        ADCS.isTurningGy(gyr_offset)
        print("Turned")
        holdPos += 1
        if holdPos == 5:
            holdPos = 1
        incrementnum = sharedQueue.put(holdPos)
        time.sleep(10)

def KeepTime():
    runTim = 0
    while True:
        runTim+=1
        timeQueue.put(runTim)
        time.sleep(1)

def getLoc(lastTime):
    CurTime = timeQueue.get() - lastTime
    return(CurTime*.14311)#multiply by the tams speed to get meters

def createGPS():
    i2c = board.I2C()
    gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)


    gps.send_command(b"PMTK220,2000")
    #sets the update rate to update GPS data every seccond
    gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    #sets the update info to GGA and RMC
    return gps

def CommsRun():
    print("Thread running!")
    while True:
        
        if not os.listdir(CorePath+"/Imaging/ToProcess"):
           
           fproc.test_imaging()
           
        for filename in os.listdir(CorePath+"/Comms/Images/"):
            #f = os.path.join(directory, filename)
            print(filename)
            Comms.send_img(filename)
               
def legfinder():
    picam2 = Picamera2()

    picam2.start()

    leg = 1

    w = True

    x = True

    duration = 135
    wait = 10

    sums = {}

    while w == True:
        
        
        
        lux_sum = 0
        
        for i in range(duration):
            time.sleep(1)
            #print(picam2.capture_metadata())
            data = picam2.capture_metadata()
            #lux_idx = data.index("'Lux'") + 7
            luxval = data["Lux"] 
            print(f"Lux Value is {luxval}")
            lux_sum += luxval   
            
        sums[leg] = lux_sum    
            
        print(f"Leg: {leg} /nLux Sum: {lux_sum}")
        
        leg += 1
        
        if leg == 5:
            break 
        
        time.sleep(wait)
        
        
        
    print(sums)

    sort = sorted(sums.items(), key=lambda x: x[1], reverse=True)
    highest = [item[0] for item in sort[0:2]]
    sorted(highest)
    print(f"Keys of the two highest values: {sorted(highest)}")

    return highest

def nightcheck():
    cam = Picamera2()    
    
    night = True
    
    cam.start()
        
    dat = cam.capture_metadata()
    
    luxva = dat["Lux"]
    
    if luxva > 50 :
        
        night = False 
    
    else:
        
        night = True
        
    cam.close()
    
    return night    

def getLeg():
    return(sharedQueue.get())

def runProcessing():
    while True:
        for i in os.listdir("/home/aaki/BWSICode/SNAC-SAT/Imaging/Masks"):
            fproc.color_id("/home/aaki/BWSICode/SNAC-SAT/Imaging/Masks"+i)

def getPow():
    return powerMan.getVolts()


thread1 = threading.Thread(target=CommsRun)
thread2 = threading.Thread(target = LegRun)
thread3 = threading.Thread(target = KeepTime)
thread4 = threading.Thread(target = runProcessing())


legtrack_known = False

def getLeg():
    return(sharedQueue.get())

thread1.start()
thread2.start()
thread3.start()
thread4.start()
legStrtTime = 0

gps = createGPS()
print(gps.update())

while True:
    
    #if we havent calibrated
    if legtrack_known == False:
        
        Image_Legs = legfinder()
        
        legtrack_known = True
        print(Image_Legs)

    

    
    legPos = getLeg()
    nigh = nightcheck()
    
    #if we're over cities
    if legPos in Image_Legs:
    
        pictures.takepic(3, legPos, nigh,timeQueue.get(),getLoc(),getPow(),gps.update())
    
    
    
    
