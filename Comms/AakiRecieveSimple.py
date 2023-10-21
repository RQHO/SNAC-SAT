import serial
import base64
import os
import sys
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(15)

filename = "QuincyTest2"

def receive_data(filename, port='/dev/ttyS0', baud_rate=9600):
#try:
    receivedBytes = bytearray("",encoding = "utf-8")

    ser = serial.Serial(port, baud_rate)
    
    rec_str = bytearray()
    dataStor = ""

    i = True
    uniqEnd = False

    rots = 0
    obj1 = b''
    obj2 = b''
    obj3 = b''
    obj4 = b''
    obj5 = b''
    RecImg = False
    RecDat = False
    while i == True:
        readden = ser.read()

        obj5 = obj4
        obj4 = obj3
        obj3 = obj2
        obj2 = obj1
        obj1 = readden
        rots += 1
        print(readden)
        print(str(obj5+obj4+obj3+obj2+obj1))
        #print(rec_str)
        #print(len(str(readden)))
        if rots >= 5:
            if str(obj5+obj4+obj3+obj2+obj1) == "b'[fin]'":
                    ser.close()
                    rec_str = rec_str
                    i = False
                    print(rec_str)
            elif str(obj5+obj4+obj3+obj2+obj1) == "b'[img]'":
                print("begin image receive")
                RecImg = True
                RecDat = False
                obj1 = b''
                obj2 = b''
                obj3 = b''
                obj4 = b''
                obj5 = b''
            elif str(obj5+obj4+obj3+obj2+obj1) == "b'[dat]'":
                RecDat = True
                RecImg = False
                obj1 = b''
                obj2 = b''
                obj3 = b''
                obj4 = b''
                obj5 = b''
                
            elif RecImg == True:
                rec_str.extend(obj5)
            elif RecDat == True:
                dataStor += obj1.decode("utf-8")
    print(dataStor)
    with open(os.path.join(sys.path[0],"DownLinkedData/"+dataStor+".jpg"), 'wb') as decodeit:
        decoded,BOTH,fixes = rsc.decode(bytes(rec_str))
        print(decoded)
        decoded = base64.b64decode(decoded)
        decodeit.write(decoded)
        print("Fixed "+str(len(fixes))+" errors/removals")
    
    """with open(filename, 'wb') as file:
        while True:
            data = ser.read()
            if not data:
                break
            file.write(data)"""
    
    print(f"Data received and saved to {filename}!")
#except Exception as e:
    #print(f"Error: {e}")

if __name__ == "__main__":
    file_to_save = os.path.join(sys.path[0],"DownLinkedData/"+filename+".jpg")  # Change to path for saved rcvie
    receive_data(file_to_save)
