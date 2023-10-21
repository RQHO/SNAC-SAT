import cv2
import numpy as np
import sys
import statistics
import os
#     np.set_printoptions(threshold=sys.maxsize)

# Script for determining the percentage of each color and the brightness of each color.
# This code is set up to run from the command line!
# When doing so, type the image file name after python IDColors.py
# Type True after if you want to see the image after the filters are applied

class fproc():
    @staticmethod
    def get_mask(image, bound):
        # Threshold returns boolean array of pixels in the image. This means that every pixel that is not that color is 0 and every
        
        threshold = cv2.inRange(image, bound[0], bound[1])
        mask = cv2.bitwise_and(image, image, mask=threshold)
        masked_image = cv2.bitwise_and(image, mask)
        
        return threshold, mask, masked_image
    @staticmethod
    def count_pixels(threshold):
        # Count the number of pixels that are each color. There are a number of ways you can do this!
        # Think about what information the threshold, mask, and mask image outputs from get_mask give you
        # You should not need to iterate over every pixel! 
        
        #<YOUR CODE GOES HERE>

        return cv2.countNonZero(threshold)
    @staticmethod
    def calc_brightness(mask):
        # Convert the filtered image to the HSV color space and extract the V channel. Remember, your image will be represented
        # as a Numpy array. Think about how Numpy will store the values. A good strategy is to use an image where you know
        # what each channel will look like and print out the numpy arrays to examine your values.
    
        hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)[:,:,2]

        # Get rid of any value that is 0 (since the mask has identified that as not the color we're looking for

        #return average_brightness
        return (np.sum(hsv))/(cv2.countNonZero(hsv))
    @staticmethod
    def bad_pic(mask):
        
        zone = 30
        
        height, width = mask.shape[:2]
        
        top_roi = mask[0:zone, 0:width-1]
        bottom_roi = mask[height - zone:height, 0:width-1]
        # Convert the ROI to grayscale
        topgray_roi = cv2.cvtColor(top_roi, cv2.COLOR_BGR2GRAY)
        bottomgray_roi = cv2.cvtColor(bottom_roi, cv2.COLOR_BGR2GRAY)
        # Check if any pixel in the ROI is not black (has nonzero intensity)
        res1 = np.any(topgray_roi != 0)
        res2 = np.any(bottomgray_roi != 0)
        
        if res1 or res2:
            
            return True
        
        else:
            
            return False


    @staticmethod
    def led_counter(mask):
        
        _, binary_mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

        result_image = cv2.merge((binary_mask, binary_mask, binary_mask))
        
        #gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        
        smooth = cv2.GaussianBlur(result_image, (5,5), 1)
        
        border = cv2.Canny(smooth, 30, 150, 3)
        
        thick = cv2.dilate(border, (1, 1), iterations=1)
        
        contours, hierarchy = cv2.findContours(thick, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        return thick, int(len(contours)), contours
        
        
        
    def color_counter(self,image):
        color_range = {}
        #TODO: the ? with what the lower and upper bounds for each color should be
        color_range["red"] = [(0, 0, 170), (50, 50, 255)]
        color_range["green"] = [(0, 140, 0), (80, 255, 80)]
        color_range["blue"] = [(100, 0, 0), (255, 80, 80)]
        color_range["yellow"] = [(0, 10, 30), (30, 80, 150)]
        color_range["white"] = [(110, 140, 110), (255, 255, 255)]   
        
        #TODO: Go up to the get_mask function and complete it! It should return
        # the threshold for each color, the mask, and the image 
        red_th, red_mask, red_mask_im = self.get_mask(image, color_range['red'])
        green_th, green_mask, green_mask_im = self.get_mask(image, color_range['green'])
        blue_th, blue_mask, blue_mask_im = self.get_mask(image, color_range['blue'])
        yellow_th, yellow_mask, yellow_mask_im = self.get_mask(image, color_range['yellow'])
        white_th, white_mask, white_mask_im = self.get_mask(image, color_range['white'])

        masks = [red_mask, green_mask, blue_mask, yellow_mask, white_mask]

        #Empty dictionary to set up getting the colors
        color_amount = {"red":0, "green":0, "blue":0, "yellow":0, "white":0}

        #TODO: Write count_pixels function!
        color_amount["red"] = self.count_pixels(red_th)
        color_amount["green"] = self.count_pixels(green_th)
        color_amount["blue"] = self.count_pixels(blue_th) 
        color_amount["yellow"] = self.count_pixels(yellow_th)  
        color_amount["white"] = self.count_pixels(white_th)
        
        total_pixels = image.shape[0] * image.shape[1]
        perc_red = color_amount["red"] / total_pixels
        perc_green = color_amount["green"] / total_pixels
        perc_blue = color_amount["blue"] / total_pixels
        perc_yellow = color_amount["yellow"] / total_pixels
        perc_white = color_amount["white"] / total_pixels
        return (perc_blue, perc_green, perc_red, perc_yellow, perc_white, masks)


    # Main code that is being run

    def color_id(self,image_file):
        folder_path = '/home/aaki/BWSICode/SNAC-SAT/Comms/Images'
        imageSave = image_file
        image_file = "/home/aaki/BWSICode/SNAC-SAT/Imaging/Masks/"+image_file  # Replace with the folder path in VScode. 
        #This is where your masks will be uploaded if you do "False" 
        #If you run as "True", your masks will pop up on the screen and will not be saved anywhere
        
        image = cv2.imread(image_file)  # Converts image to numpy array in BGR format

        #TODO: Write the color counter function!
        perc_blue, perc_green, perc_red, perc_yellow, perc_white, masks = self.color_counter(image)

        """print("The percentage of red is", round(100 * perc_red, 2), "%")
        print("The percentage of green is", round(100 * perc_green, 2), "%")
        print("The percentage of blue is", round(100 * perc_blue, 2), "%")
        print("The percentage of yellow is", round(100 * perc_yellow, 2), "%")
        print("The percentage of white is", round(100 * perc_white, 2), "%")"""
        
        red_mask = masks[0]
        green_mask = masks[1]
        blue_mask = masks[2]
        yellow_mask = masks[3]
        white_mask = masks[4]

        # If the show flag is set to true, this will set up images to visualize the color ID.
        # Note: if you're on a windows machine and haven't set up X11 forwarding,
        # this won't work. If show is set to False, the image masks will be stored to
        # the images/ folder
        
        bad = False
        
        for item in masks:
            
            if self.bad_pic(item) == True:

                bad = True
                print("Bad Pic")
                break
            
        if not bad:     
            """cv2.imwrite(folder_path + '/blue_mask.jpg', blue_mask)
            cv2.imwrite(folder_path + '/green_mask.jpg', green_mask)
            cv2.imwrite(folder_path + '/red_mask.jpg', red_mask)
            cv2.imwrite(folder_path + '/yellow_mask.jpg', yellow_mask)
            cv2.imwrite(folder_path + '/white_mask.jpg', white_mask)"""
            print('Image masks saved')
            
            cv2.imwrite(folder_path + '/blue_blur.jpg', self.led_counter(blue_mask)[0])
            cv2.imwrite(folder_path + '/green_blur.jpg', self.led_counter(green_mask)[0])
            cv2.imwrite(folder_path + '/red_blur.jpg', self.led_counter(red_mask)[0])
            cv2.imwrite(folder_path + '/white_blur.jpg', self.led_counter(white_mask)[0])
            cv2.imwrite(folder_path + '/yellow_blur.jpg', self.led_counter(yellow_mask)[0])
            print('Image blurs saved')
        
        if self.led_counter(blue_mask)[1]+self.led_counter(green_mask)[1]+self.led_counter(red_mask)[1]+self.led_counter(yellow_mask)[1]+self.led_counter(white_mask)[1] == 0:
            
            bad = True
            print("No LEDs")
            
        if not bad:    
            blue_leds = self.led_counter(blue_mask)[1]
            green_leds = self.led_counter(green_mask)[1]
            red_leds = self.led_counter(red_mask)[1]
            yellow_leds = self.led_counter(yellow_mask)[1]
            white_leds = self.led_counter(white_mask)[1]
            
            print(f"Blue LEDs: {self.led_counter(blue_mask)[1]}")
            print(f"Green LEDs: {self.led_counter(green_mask)[1]}")
            print(f"Red LEDs: {self.led_counter(red_mask)[1]}")
            print(f"Yellow LEDs: {self.led_counter(yellow_mask)[1]}")
            print(f"White LEDs: {self.led_counter(white_mask)[1]}")
            print(f"Total LEDs: {self.led_counter(blue_mask)[1]+self.led_counter(green_mask)[1]+self.led_counter(red_mask)[1]+self.led_counter(yellow_mask)[1]+self.led_counter(white_mask)[1]}")

            #PART 2: BRIGHTNESS. Uncomment this when you are ready!
            #TODO: Write calc_brightness!
            red_brightness = self.calc_brightness(red_mask)
            green_brightness = self.calc_brightness(green_mask)
            blue_brightness = self.calc_brightness(blue_mask)
            yellow_brightness = self.calc_brightness(yellow_mask)
            white_brightness = self.calc_brightness(white_mask)
            
            """print("The brightness of red is", round(red_brightness, 3))
            print("The brightness of green is", round(green_brightness, 3))
            print("The brightness of blue is", round(blue_brightness, 3))
            print("The brightness of yellow is", round(yellow_brightness, 3))
            print("The brightness of white is", round(white_brightness, 3))"""
            
            avg_brt = round(statistics.fmean([red_brightness, green_brightness, blue_brightness, yellow_brightness, white_brightness]), 3)
            print(f"Avg Brightness: {avg_brt}")

            
            os.replace(image_file,folder_path+imageSave)
            os.rename(folder_path+imageSave,folder_path+imageSave+("{avg_brt}_"+str({self.led_counter(red_mask)[1]})+str({self.led_counter(blue_mask)[1]})+str({self.led_counter(green_mask)[1]})+str({self.led_counter(yellow_mask)[1]})+str({self.led_counter(white_mask)[1]})))
            return({avg_brt},{self.led_counter(red_mask)[1]},{self.led_counter(blue_mask)[1]},{self.led_counter(green_mask)[1]},{self.led_counter(yellow_mask)[1]},{self.led_counter(white_mask)[1]},)
