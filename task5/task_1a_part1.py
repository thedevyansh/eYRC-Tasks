'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ 2650 ]
# Author List:		[ Devyansh Chawla, Hardik Sharma, Shikhhar Siingh ]
# Filename:			task_1a_part1.py
# Functions:		[ scan_image, update_dictionary, detect_shape_color, line_length, find_quadrilateral_type ]
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

# detect_shape_color() returns the color of detected shape
def detect_shape_color(original_img, centroid_x, centroid_y):
    if original_img[centroid_y, centroid_x, 2] == np.array([0, 0, 255], dtype=np.uint8)[2]:
        return 'red'
    elif original_img[centroid_y, centroid_x, 0] == np.array([255, 0, 0], dtype=np.uint8)[0]:
        return 'blue'
    else:
        return 'green'

# line_length() returns the length of side of quadrilateral
#def line_length(x1, y1, x2, y2):
#    length = ((x1-x2)**2 + (y1-y2)**2)**0.5
#    return length

# find_quadrilateral_type() return the type of quadrilateral like sqaure, rhombus etc.
#def find_quadrilateral_type(approx):
#    coords = approx.ravel()
#    x = np.array([coords[0], coords[2], coords[4], coords[6]])
#    y = np.array([coords[1], coords[3], coords[5], coords[7]])
#
#    adjacent_sides_ratio = line_length(
#        x[0], y[0], x[1], y[1])/line_length(x[1], y[1], x[2], y[2])
#    diagonal_ratio = line_length(
#        x[0], y[0], x[2], y[2])/line_length(x[1], y[1], x[3], y[3])
#    opposite_sides_ratio = line_length(
#        x[0], y[0], x[1], y[1])/line_length(x[2], y[2], x[3], y[3])
#
#    slope1 = (y[1] - y[0]) / (x[1] - x[0]) if x[1] != x[0] else 1
#    slope2 = (y[2] - y[1]) / (x[2] - x[1]) if x[1] != x[2] else 1
#    slope3 = (y[3] - y[2]) / (x[3] - x[2]) if x[3] != x[2] else 1
#    slope4 = (y[0] - y[3]) / (x[0] - x[3]) if x[3] != x[0] else 1
#
#    slope_ratio1 = slope1 / slope3
#    slope_ratio2 = slope2 / slope4
#
#    if (slope_ratio1 >= 0.95 and slope_ratio1 <= 1.05) or (slope_ratio2 >= 0.95 and slope_ratio2 <= 1.05):
#        if opposite_sides_ratio >= 0.95 and opposite_sides_ratio <= 1.05:
#            if adjacent_sides_ratio >= 0.95 and adjacent_sides_ratio <= 1.05:
#                if diagonal_ratio >= 0.95 and diagonal_ratio <= 1.05:
#                    return 'Square'
#                else:
#                    return 'Rhombus'
#            else:
#                return 'Parallelogram'
#        else:
#            return 'Trapezium'
#    else:
#        return 'Quadrilateral'

##############################################################

def scan_image(original_img):
    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }

    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes

    shapes = {}

    ##############	ADD YOUR CODE HERE	##############

    grayscale_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([25,20,20])
    upper_bound = np.array([86,255,255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    #cv2.imshow("ret", mask)
    #cv2.waitKey(1)

    #_, threshold = cv2.threshold(grayscale_img, 200, 255, cv2.THRESH_BINARY)
    #cv2.imshow("ret",threshold)
    #cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    height, width, channel = original_img.shape
    shapelist = []

    for cnt in contours:

        if cv2.contourArea(cnt) > (0.995 * width * height): #this is used to exclude parent element from being considered as a contour
            continue
        #approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        #print(cv2.contourArea(cnt))
        #print(cv2.contourArea(cnt))
        x, y, w, h = cv2.boundingRect(cnt)

        cx = int(x + w / 2)
        cy = int(y + h / 2)

        #M = cv2.moments(cnt)
        #cx = int(M['m10']/M['m00'])
        #cy = int(M['m01']/M['m00'])

        shape_color = detect_shape_color(original_img, cx, cy)
        shapelist.append([shape_color, cx, cy])
    
    #cv2.drawContours(original_img, contours, -1, (0, 0, 255), 5)
    #cv2.imshow("ret", original_img)
    #cv2.waitKey(0)

    if(len(shapelist) == 1):
        shapes.update({'Circle':[shapelist[0][0],shapelist[0][1],shapelist[0][2]]})    
    else:
        shapelist = sorted(shapelist, key = lambda x : x[0])
        shapes.update({'Circle':shapelist})

    ##################################################

    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in ' + curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'

    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')

    else:
        print('\n[ERROR] Sample' + str(file_num) +
              '.png not found. Make sure "Samples" folder has the selected file.')
        exit()

    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' +
              img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')

        else:
            print('\n[ERROR] scan_image function returned a ' +
                  str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print(
            '\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input(
        '\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2

        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + \
                'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')

            else:
                print('\n[ERROR] Sample' + str(file_num + 1) +
                      '.png not found. Make sure "Samples" folder has the selected file.')
                exit()

            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' +
                      img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')

                else:
                    print('\n[ERROR] scan_image function returned a ' +
                          str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print(
                    '\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
