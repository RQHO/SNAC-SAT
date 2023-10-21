import serial
import base64
import os
import sys
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(15)

class ReceiveData:
    def receive_data(port='/dev/ttyS0', baud_rate=9600):
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
                    dataStor += obj5
        print(dataStor)
        dataStor = (rsc.decode(dataStor)).decode("utf-8")
        decodeit = open(os.path.join(sys.path[0],"DownLinkedData/"+dataStor+".jpg"), 'wb')
        decoded,BOTH,fixes = rsc.decode(bytes(rec_str))
        print(decoded)
        decoded = base64.b64decode(decoded)
        decodeit.write(decoded)
        print("Fixed "+str(len(fixes))+" errors/removals")
        
        print(f"Data received and saved to {dataStor}!")
        
        return extract_telemetry(dataStor)
        
    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def extract_telemetry(filename= "abc_def_ghi_jkl_mno_1_2_3_4_5_6.jpg"):

        unjpg = filename[0:-4]

        x = find(unjpg, "_")

        if len(x) != 10:

            print(f"Error Decoding, Interpret Manually:  file {filename}")

            return {"Filename": filename, "Data": False}

        else:

            leg = unjpg[0:x[0]]
            dist = unjpg[x[0]+1:x[1]]
            power = unjpg[x[1]+1:x[2]]
            gps = unjpg[x[2]+1:x[3]]
            time = unjpg[x[3]+1:x[4]]
            avbrt = unjpg[x[4]+1:x[5]]
            red = unjpg[x[5]+1:x[6]]
            blue = unjpg[x[6]+1:x[7]]
            green = unjpg[x[7]+1:x[8]]
            yellow = unjpg[x[8]+1:x[9]]
            white = unjpg[x[9]+1:]


            print(filename)
            print(f"Leg: {leg}")
            print(f"Dist: {dist}")
            print(f"Power: {power}")
            print(f"GPS: {gps}")
            print(f"Time: {time}")
            print(f"Avg Brightness: {avbrt}")
            print(f"Red LEDs: {red}")
            print(f"Blue LEDs: {blue}")
            print(f"Green LEDs: {green}")
            print(f"Yellow LEDs: {yellow}")
            print(f"White LEDs: {white}")

            tot = int(red) + int(blue) + int(green) + int(yellow) + int(white)

            print(f"Total LEDs: {tot}")

            return {"Filename": filename, "Data": True, "Leg": leg, "Dist": dist, "Power": power, "Time": time, "Avg Brightness": avbrt, "Red LEDs": red, "Blue LEDs": blue, "Green LEDs": green, "Yellow LEDs": yellow, "White LEDs": white, "Total LEDs": tot}
