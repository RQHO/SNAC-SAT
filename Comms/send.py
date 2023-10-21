from reedsolo import RSCodec, ReedSolomonError
#INSTALL ON SUDO LEVEL
import serial
import base64
import os
import sys

class CommSend:
    rsc = RSCodec(15)

    def __init__(self):
        print("Initialized comms")


    #main function. takes a filename, converts to base 64, writes, sends.
    def send_img(self,filename, port='/dev/ttyUSB0', baud_rate=9600):
        print("Begin convert")


        #Read the image and encode
        with open(os.path.join(sys.path[0],"Images/"+filename), "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())
            #converted_string = base64.b64encode(converted_string)
            y = converted_string#.decode("utf-8")
        os.replace(os.path.join(sys.path[0],"Images/"+filename),os.path.join(sys.path[0],"SentImages/"+filename))
        y = self.rsc.encode(y)
        print(y)

        print("Converted as "+str(len(y))+" characters")
        #Write to file
        written = open(os.path.join(sys.path[0],"ConvertedImages/"+filename.replace(filename[len(filename)-4:],"")+".txt"), "w")
        written.write(str(y))
        print("File created")

        #Attempts data send
        try:
            ser = serial.Serial(port, 9600)
            z = open(os.path.join(sys.path[0],"ConvertedImages/"+filename.replace(filename[len(filename)-4:],"")+".txt"), "rb")
            
            data = z.read()

            data = y
            ser.write(b"[img]")
            ser.write(data)
            ser.write(b"[dat]")
            ser.write(self.rsc.encode(filename.replace(filename[len(filename)-4:],""),"utf-8"))
            ser.write(b"[fin]")
            print(f"Data sent successfully from {filename}!")
        except Exception as e:
            print(f"Error: {e}")


    #file_to_send = "TestColors.jpg"
    #send_data(file_to_send)
