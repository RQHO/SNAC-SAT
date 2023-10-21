from reedsolo import RSCodec, ReedSolomonError
#INSTALL ON SUDO LEVEL
import serial
import base64
import os
import sys

class CommSend:

    ImageQueue = [[],[]]
    rsc = RSCodec(15)

    def __init__(self):
        print("Initialized comms")


    #main function. takes a filename, converts to base 64, writes, sends.
    def send_data(self,filename, port='/dev/ttyS0', baud_rate=9600):
        print("Begin convert")


        #Read the image and encode
        with open(os.path.join(sys.path[0],"Images/"+filename), "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())
            #converted_string = base64.b64encode(converted_string)
            y = converted_string#.decode("utf-8")

        y = self.rsc.encode(y)
        print(y)

        print("Converted as "+str(len(y))+" characters")
        #Write to file
        written = open(os.path.join(sys.path[0],"ConvertedImages/"+filename.replace(filename[len(filename)-4:],"")+".txt"), "w")
        written.write(str(y))
        print("File created")

        #Attempts data send
        try:
            ser = serial.Serial('/dev/ttyS0', 9600)
            z = open(os.path.join(sys.path[0],"ConvertedImages/"+filename.replace(filename[len(filename)-4:],"")+".txt"), "rb")
            
            data = z.read()
            data = y
            ser.write(data)
            ser.write(b"[fin]")
            print(f"Data sent successfully from {filename}!")
        except Exception as e:
            print(f"Error: {e}")


    #file_to_send = "TestColors.jpg"
    #send_data(file_to_send)