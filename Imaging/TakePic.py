from picamera2 import Picamera2
import time

class pictake:
    
    def takepic(frequency=3, leg=1, night = True,timmeh = 0, dist=0, pow = 0, gps = False):

        # Accepts frequency as a floating point number of seconds
        # leg as the current orbital leg as an integer (1, 2, 3, or 4)
        # night as True or False for whether the time is true or false
        # dismount 
        
        r1 = 200
        r2 = 200

        if night == True:
        
            exposure = 150
            exposurevalue = 8.0

            cgr = 1.5
            cgb = 1
            
            tim = "nht"
        
        
        else:
            
            exposure = 150
            exposurevalue = 8.0

            cgr = 1.5
            cgb = 1   

            tim = "day"
            

        camera = Picamera2()

        main = {"size": (r1, r2)}
        
        camera_config = camera.create_still_configuration(main={"size": (1640, 922)})
        camera.configure(camera_config)
        camera.set_controls({"ExposureTime": exposure, "AnalogueGain": 1.0, "ExposureValue": exposurevalue, "ColourGains": (cgr, cgb)})

        camera.start()

    
            
        t = time.strftime("_%H%M%S")

        #camera.capture_file(f"/home/aaki/BWSICode/SNAC-SAT/Comms/Images/{t}_{tim}.jpg")
        camera.capture_file(f"/home/aaki/BWSICode/SNAC-SAT/Imaging/Images/{leg}_{dist}_{pow}_{gps}_{timmeh}.jpg")
        
            
        print("PicTaken")
        
        camera.close() 
