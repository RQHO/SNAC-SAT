import serial
import os
import sys

#sets up the xbee serial port (same constraints as the XCTU interface)
ser = serial.Serial(
        port = "/dev/ttyS0"
           #TODO: fill in with the port information
         )

#writes the signal start to the other XBee

def sendImage(file):
  print("sending file now")
  with open(os.path.join(sys.path[0],"ConvertedImages/"+ file), 'r') as fp:
    for count, line in enumerate(fp):
      pass
  ser.write(b'<IMGSTRT>')
  print(count)
  stream = open(os.path.join(sys.path[0], "ConvertedImages/"+file), 'rb') #<-- Replace with the file path to the file to send over the XBees
  #copies contents of a file to the variable 'data'
  print("Converted")
  data = stream.read()
  ser.write(data)

def sendTellemPackage(data):
  ser.write(b'<DATASTRT>')
  ser.write(data)

print("Writing data now")

sendImage("TestColors.txt")
ser.write(bytes("<ENDSEND>","ascii"))


print("Data written")
