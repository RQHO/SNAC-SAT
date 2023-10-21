from multiprocessing import Value
from turtle import color
from PIL import Image
import os
import sys
import serial
from itertools import chain
import math

TestName = "TestColors"
test = True
#sets up the xbee serial port (same constraints as the XCTU interface)



def decode_from_8bit(encoded_image_path, color_palette):
    encoded_image = Image.open(encoded_image_path)

    # Convert the image to an array
    encoded_pixels = np.array(encoded_image)

    # Replace indices with RGB values from the palette
    decoded_pixels = color_palette[encoded_pixels]

    # Create the decoded image and save it
    decoded_image = Image.fromarray(np.uint8(decoded_pixels))
    decoded_image.save("decoded_image.png")

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

def convert_8bit_to_rgb(color_index):
    return color_index

def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    print(len(flat_list))
    return flat_list

def create_image(hex_list,pallet):
    totalChar = 0
    for i in hex_list:
        totalChar += len(i)
    print("Total: "+str(totalChar))
    totalChar = totalChar/len(hex_list)

    height = len(hex_list)

    width = math.ceil(totalChar)

    #while (width/height)%2 != 0:
    #    width+= 1

    width = len(hex_list[0])
    print(width)
    print(height)
    hex_list = flatten_extend(hex_list)
    print("Expected: "+str(width*height))
    print(type(hex_list))
    print(len(hex_list))
    #print(hex_list[0])
    # Create a new blank image with the specified dimensions
    image = Image.new('P', (width, height))
    image.putpalette(pallet)
    #print("Heres the list "+ str(flatten_extend(hex_list)))
    #print(hex_list[0])
    image.putdata(hex_list)

    image = image.convert("RGB")

    return image

def decodeImages(string):
    newList = string.split("<ENDRW>")
    newList = [i.split(",") for i in newList]
    expandedList = []
    currentPix = 0
    for row in newList:
        tempList = []
        for index in row:
            holdpix = index.split("-")
            try:
                if len(holdpix) > 1:
                    if holdpix[1].isdigit():  # Check if the second element is a digit
                        for i in range(int(holdpix[1])):
                            tempList.append(int(holdpix[0]))
                    else:
                        tempList.append(int(holdpix[0]))
                elif isinstance(holdpix,list):
                    if holdpix[0] == "":
                        tempList.append(255)
                    else:
                        tempList.append(int(holdpix[0]))
                else:
                    if holdpix == "":
                        tempList.append(255)
                    else:
                        tempList.append(int(holdpix))
            except ValueError:
                print("haha you got a bad bit of data")
                tempList.append(255)
        expandedList.append(tempList)
    print("finished reconstructing")
    return expandedList


def get_substring_between_words(input_string, word1, word2):
    start_index = input_string.find(word1)
    end_index = input_string.find(word2)

    if start_index == -1 or end_index == -1:
        return None

    start_index += len(word1)
    return input_string[start_index:end_index].strip()

# Opens the file to store the recieved data in
#loop to receive data
lines = "hai :3 something has gone tewwiwby wrong :D"

if test:
    with open(os.path.join(sys.path[0], "ConvertedImages/"+TestName+".txt")) as f:
        lines = "".join(line.strip() for line in f)
    #print(lines)
else:
    ser=serial.Serial(
    port = "/dev/ttyS0", #change to xbee port
    )
    fullString = ""
    last = ""
    while True:
        #recieves data over serial port
        rec = str(ser.read().decode("ascii"))
        fullString+=rec
        print(rec)
        if fullString[len(fullString) - 8:] == "<ENDSEND>" or (last == "D" and rec == ">"):
            print("Received end transmission message")
            break
        last = rec
    lines = fullString
    ser.close()
        #saves recieved data to the file

#Test code (uses stored files)

#f= open(os.path.join(sys.path[0], "ConvertedImages\\"+TestName+".txt"),"w+")

#with open(os.path.join(sys.path[0], "ConvertedImages/"+TestName+".txt")) as f:
#    lines = "".join(line.strip() for line in f)
#print(lines)

pallet = get_substring_between_words(lines,"<PALSTAR>[","]<PALEN>")
lines = lines.replace("<PALSTAR>["+pallet+"]<PALEN>", "")
#lines = lines.replace("]<PALEND>", "")
lines = lines.replace(" ", "")
print(len(lines))
pallet = list(pallet.split(","))
#print(pallet)
for i in range(len(pallet)):
    pallet[i] = int(pallet[i])
#print(pallet)
print("Printing pallet")
print(pallet)
print("Pallet printed")
#print(flatten_extend(pallet))
print(lines)
finishedArr = decodeImages(lines)
print("Decoded: "+str(len(finishedArr[0])))
#print(finishedArr)
img = create_image(finishedArr, pallet)
#print(finishedArr)
img.save(TestName+"Reconstructed.png")


#imageSV = open(os.path.join(sys.path[0], "DownlinkedData/"+TestName+".png"))

#create_image_from_hex_list(finishedArr,TestName+"Reconstructed.png")

#f.write(rec)