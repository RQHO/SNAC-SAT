import cv2 as cv
import numpy as np
import sys
import statistics

def get_mask(image, bound):
    """
    Returns a mask of the image with the specified color range.

    Args:
        image: The image to be masked.
        bound: A tuple of two tuples, each containing the lower and upper bounds of the color range.
    
    Returns:
        threshold: The thresholded image.
        mask: The masked image.
        masked_image: The image with the mask applied.
    """
    lower_bound = np.array(bound[0])
    upper_bound = np.array(bound[1])

    threshold = cv.inRange(image, lower_bound, upper_bound)
    mask = cv.bitwise_and(image, image, mask = threshold)
    masked_image = cv.bitwise_and(image, mask)

    return threshold, mask, masked_image

def get_LED_count(mask):
    """
    Returns the number of LEDs in the image.

    Args:
        mask: The masked image.
    
    Returns:
        count: The number of LEDs in the image.
    """
    gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    smooth = cv.GaussianBlur(gray, (5, 5), 1)
    border = cv.Canny(smooth, 30, 150, 3)
    thick = cv.dilate(border, (1, 1), iterations=1)
    contours, hierarchy = cv.findContours(thick, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    count = len(contours)
    return count

def get_color_masks(image):
    """
    Returns a list of masks for each color.

    Args:
        image: The image to be masked.

    Returns:
        masks: A list of masks for each color.
    """
    # BGY
    color_range = {
        'red': [(0, 0, 100), (80, 80, 255)],
        'green': [(0, 100, 0), (80, 255, 80)],
        'blue': [(100, 0, 0), (255, 80, 80)],
        'yellow': [(0, 100, 100), (80, 255, 255)],
        'white': [(200, 200, 200), (255, 255, 255)]
    }

    red_mask = get_mask(image, color_range['red'])[1]
    green_mask = get_mask(image, color_range['green'])[1]
    blue_mask = get_mask(image, color_range['blue'])[1]
    yellow_mask = get_mask(image, color_range['yellow'])[1]
    white_mask = get_mask(image, color_range['white'])[1]

    masks = [red_mask, green_mask, blue_mask, yellow_mask, white_mask]
    
    return masks

def get_average_brightness(mask):
    """
    Returns the average brightness of the image.

    Args:
        mask: The masked image.
    
    Returns:
        average: The average brightness of the image.
    """

    hsv = cv.cvtColor(mask, cv.COLOR_BGR2HSV)[:, :, 2]
    if cv.countNonZero(hsv) == 0:
        return 0
    average = np.sum(hsv) / cv.countNonZero(hsv)
    return average

def test_imaging(file, show = False):
    folder = 'Masks/'

    image = cv.imread(file)

    masks = get_color_masks(image)
    num_red = get_LED_count(masks[0])
    num_green = get_LED_count(masks[1])
    num_blue = get_LED_count(masks[2])
    num_yellow = get_LED_count(masks[3])
    num_white = get_LED_count(masks[4])
    total_LEDs = num_red + num_green + num_blue + num_yellow + num_white

    print('Red LEDs:', num_red)
    print('Green LEDs:', num_green)
    print('Blue LEDs:', num_blue)
    print('Yellow LEDs:', num_yellow)
    print('White LEDs:', num_white)
    print('Total LEDs:', total_LEDs)

    red_brightness = get_average_brightness(masks[0])
    green_brightness = get_average_brightness(masks[1])
    blue_brightness = get_average_brightness(masks[2])
    yellow_brightness = get_average_brightness(masks[3])
    white_brightness = get_average_brightness(masks[4])
    
    # Calulate average brightness, ignoring 0 values
    brightnesses = [red_brightness, green_brightness, blue_brightness, yellow_brightness, white_brightness]
    brightnesses = [x for x in brightnesses if x != 0]
    average_brightness = statistics.mean(brightnesses)
    print("Average Brightness: ", round(average_brightness, 3))

    if show:
        cv.imshow('Red Mask', masks[0])
        cv.imshow('Green Mask', masks[1])
        cv.imshow('Blue Mask', masks[2])
        cv.imshow('Yellow Mask', masks[3])
        cv.imshow('White Mask', masks[4])

        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        cv.imwrite(folder + 'red_mask.jpg', masks[0])
        cv.imwrite(folder + 'green_mask.jpg', masks[1])
        cv.imwrite(folder + 'blue_mask.jpg', masks[2])
        cv.imwrite(folder + 'yellow_mask.jpg', masks[3])
        cv.imwrite(folder + 'white_mask.jpg', masks[4])

if __name__ == '__main__':
    test_imaging("test.jpg")