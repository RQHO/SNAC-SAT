from hmac import new
from lib2to3.pytree import convert
from turtle import clone
from PIL import Image
import os
import sys
import numpy as np
import re

#so that I don't need to change the file name a bajillion times
TestName = "TestColors"
FileType = ".jpg"
CompiledName = TestName+FileType




def generate_custom_palette():
    custom_palette = []
    
    # Red shades
    for r in range(0, 256, 51):
        custom_palette.append((r, 0, 0))
    
    # Green shades
    for g in range(0, 256, 51):
        custom_palette.append((0, g, 0))
    
    # Blue shades
    for b in range(0, 256, 51):
        custom_palette.append((0, 0, b))
    
    # Yellow shades
    for y in range(0, 256, 51):
        custom_palette.append((y, y, 0))
    
    # White/grey shades
    for w in range(0, 256, 51):
        custom_palette.append((w, w, w))
    
    # Fill the rest of the palette with black (0, 0, 0)
    remaining_slots = 256 - len(custom_palette)
    custom_palette.extend([(0, 0, 0)] * remaining_slots)
    
    return custom_palette






#return info about image
def get_Image_Info():
    img = Image.open(os.path.join(sys.path[0], "Images/"+CompiledName))
    SizeX, SizeY = img.size
    return(SizeX, SizeY)

def rgb_to_hex(r,g,b):
    #print("RGB convert has been called")
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)


def image_to_8bit_array(image_file,pallet):
    # Load the image
    image = image_file

    # Convert the image to 8-bit color palette mode
    image_8bit = image.convert("P", palette=pallet, colors=256)

    # Get the pixel values as a list
    pixel_values = np.asarray(image_8bit)

    return pixel_values

#write everything to file and convert bmp
def create_File(Name,BMP,pallet):
    print("Creating file...")
    #create a new file with image name
    f= open(os.path.join(sys.path[0], "ConvertedImages/"+TestName+".txt"),"w+")
    f.write("<PALSTAR>"+str(pallet)+"<PALEN>\n")
    SizeX, SizeY = get_Image_Info()
    print(SizeX)
    print(SizeY)
    count = 0
    for row in BMP:
        count+=1
        colCount = 1
        for col in row:
            if colCount >= len(row):
                f.write(str(col))
            else:
                f.write(str(col)+",")
            colCount+=1
        f.write("<ENDRW>\n")
        print("Completed row: "+str(count))

    print("Finished writing all data!")

#function for compressing the rows based on like-pixels
def combine_like_values(row):
    result = []
    current_object = None
    count = 0

    for value in row:
        if value != current_object:
            if current_object is not None:
                if count > 1:
                    result.append(f"{current_object}-{count}")
                else:
                    result.append(f"{current_object}")

            current_object = value
            count = 1
        else:
            count += 1

    # Append the last sequence
    if current_object is not None:
        if count > 1:
            result.append(f"{current_object}-{count}")
        else:
            result.append(f"{current_object}")

    # Special case for an entire row with the same value
    if len(result) == 0:
        if count > 1:
            result.append(f"{current_object}-{count}")
        else:
            result.append(f"{current_object}")

    return result

#for counting the number of pixels it should have
def extract_counts(row):
    counts = []
    
    for value in row:
        if '-' in value:
            _, count = value.split('-')
            counts.append(int(count))
        else:
            counts.append(1)
            
    return counts

#for fixing possible double digits
def edit_row_objects(row, total_objects):
    current_count = 0
    current_object = None
    total_count = 0
    delete_second = False

    for value in row:
        if '-' in value:
            object_, count = value.split('-')
            count = int(count)
        else:
            object_ = value
            count = 1

        if current_object is None:
            current_object = object_

        if current_object != object_:
            if current_count > 0:
                total_count += current_count

            if current_count == 2 * total_objects:
                delete_second = True

            current_object = object_
            current_count = count
        else:
            current_count += count

    if current_count > 0:
        total_count += current_count

    if current_count == 2 * total_objects:
        delete_second = True

    if delete_second and len(row) > 1:
        row.pop(1)

    if total_count == total_objects:
        return row
    else:
        # Return the original unedited row
        return row



def clean_Data(given):
    newArr = np.empty(shape = (len(given),len(given[0])), dtype = object)

    #first things first, get rid of all those crummy rgb values
    rowCount = 0
    for row in given:
        colCount = 0
        for col in row:
            r,g,b = col
            newArr[rowCount][colCount] = str(rgb_to_hex(r,g,b))
            
            colCount += 1
        rowCount+=1
    given = newArr.copy()
    print(given[0,0])
    return given

def convert_array_to_strings(input_array):
    string_array = [[str(element) for element in row] for row in input_array]
    return string_array

def optimize_Data(given):
    print("Cleaning up data...")

    print("Completed RGB to HEX conversion, beginning grouped pixel cleanse")
    newArr = []
    rowCount = -1
    for row in given:
        rowCount+=1
        X, Y = get_Image_Info()
        Converted = edit_row_objects(combine_like_values(row),X)
        newArr.append(Converted)
        #print(newArr[rowCount])
                
    print("Completed length: "+str(len(newArr)))
    return(newArr)

#gather image and convert to bitmap array
img = Image.open(os.path.join(sys.path[0], "Images/"+CompiledName))
#pallet = generate_custom_palette()

#img = image_to_8bit_array(img,pallet)
#pallet, img = encode_to_8bit(img)
img =img.convert("P", dither=Image.NONE, palette=Image.ADAPTIVE)
x,y = get_Image_Info()
pallet = img.getpalette()
img = np.array(list(img.getdata())).reshape(y,x)
print(pallet)
img = convert_array_to_strings(img)


#img = clean_Data(img)
img = optimize_Data(img)
create_File(TestName,img,pallet)
#print(img)