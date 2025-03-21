'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 5 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:          [ Team-ID ]
# Author List:      [ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:         task_5.py
# Functions:
#                   [ Comma separated list of functions in this file ]
# Global variables:
# 					[ List of global variables defined in this file ]

# NOTE: Make sure you do NOT call sys.exit() in this code.

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
import os
import sys
import traceback
import time
import math
import json
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')


# Import 'task_1b.py' file as module
try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_1a_part1.py' file as module
try:
    import task_1a_part1

except ImportError:
    print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1a_part1.py is present in this current directory.\n')


except Exception as e:
    print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_2a.py' file as module
try:
    import task_2a

except ImportError:
    print('\n[ERROR] task_2a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_2b.py' file as module
try:
    import task_2b

except ImportError:
    print('\n[ERROR] task_2b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_3.py' file as module
try:
    import task_3

except ImportError:
    print('\n[ERROR] task_3.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_3.py is present in this current directory.\n')


except Exception as e:
    print('Your task_3.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_4a.py' file as module
try:
    import task_4a

except ImportError:
    print('\n[ERROR] task_4a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_4a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_4a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

##############################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    send_color_and_collection_box_identified
#        Inputs:    ball_color and collection_box_name
#       Outputs:    None
#       Purpose:    1. This function should only be called when the task is being evaluated using
# 					   test executable.
#					2. The format to send the data is as follows:
#					   'color::collection_box_name'
def send_color_and_collection_box_identified(ball_color, collection_box_name):

    global client_id

    color_and_cb = ball_color + '::' + collection_box_name
    inputBuffer = bytearray()
    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id, 'evaluation_screen_respondable_1',
                                                                                        sim.sim_scripttype_childscript, 'color_and_cb_identification', [], [], color_and_cb, inputBuffer, sim.simx_opmode_blocking)

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


def convert_path_to_pixels(path):
    pixel_path = []

    for duo in path:
        temp = ()
        for elem in duo:
            elem = (elem * 70 + 35) + 50
            #elem = int(elem + (1 / 9) * (400 - elem))
            temp = temp + (elem, )
        # print(temp)
        pixel_path.append(temp)
    return pixel_path


def send_data_to_draw_path(rec_client_id, path, tag):
    client_id = rec_client_id

    coppelia_sim_coord_path = []

    for coord in path:
        for element in coord:
            coppelia_sim_coord_path.append(((10*element) - 45)/100)

    inputBuffer = bytearray()
    table = 'top_plate_respondable_t' + str(tag) + '_1'

    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,
                                                                                        table, sim.sim_scripttype_customizationscript, 'drawPath', [],
                                                                                        coppelia_sim_coord_path, [], inputBuffer, sim.simx_opmode_blocking)

##############################################################


def main(rec_client_id):
    """
    Purpose:
    ---

    Teams are free to design their code in this task.
    The test executable will only call this function of task_5.py.
    init_remote_api_server() and exit_remote_api_server() functions are already defined
    in the executable and hence should not be called by the teams.
    The obtained client_id is passed to this function so that teams can use it in their code.

    However NOTE:
    Teams will have to call start_simulation() and stop_simulation() function on their own.

    Input Arguments:
    ---
    `rec_client_id` 	:  integer
        client_id returned after calling init_remote_api_server() function from the executable.

    Returns:
    ---
    None

    Example call:
    ---
    main(rec_client_id)

    """
    ##############	ADD YOUR CODE HERE	##############

    client_id = rec_client_id

    # print(1)
    """Reading maze images"""
    table_1 = cv2.imread('maze_t1.jpg')
    table_4 = cv2.imread('maze_t4.jpg')

    """Warping the maze images"""
    warped_img_1 = task_1b.applyPerspectiveTransform(table_1)
    warped_img_4 = task_1b.applyPerspectiveTransform(table_4)

    """Extracting maze arrays"""
    maze_array_1 = task_1b.detectMaze(warped_img_1)
    maze_array_4 = task_1b.detectMaze(warped_img_4)

    """Modifiyng maze arrays"""
    maze_array_1[0][4] -= 2
    maze_array_1[4][9] -= 4
    maze_array_1[9][5] -= 8
    maze_array_4[5][9] -= 4

    """Sending maze array data to CoppeliaSim"""
    return_code = task_2b.send_data(client_id, maze_array_1, 1)
    return_code = task_2b.send_data(client_id, maze_array_4, 4)

    """Starting simulation"""
    task_2a.start_simulation()

    """Retrieving all the handles"""
    task_3.init_setup(client_id)
    return_code, vision_sensor_1 = sim.simxGetObjectHandle(
        client_id, 'vision_sensor_1', sim.simx_opmode_blocking)
    return_code, vision_sensor_4 = sim.simxGetObjectHandle(
        client_id, 'vision_sensor_4', sim.simx_opmode_blocking)
    return_code, vision_sensor_5 = sim.simxGetObjectHandle(
        client_id, 'vision_sensor_5', sim.simx_opmode_blocking)

    """Defining start and end coords for the different tables"""
    t1_start = (5, 0)
    t1_end = (4, 9)
    t4_start = (0, 5)
    t4_end = (5, 9)

    """Finding path for the tables"""
    path_1 = task_4a.find_path(maze_array_1, t1_start, t1_end)
    path_4 = task_4a.find_path(maze_array_4, t4_start, t4_end)

    #send_data_to_draw_path(client_id, path_4)

    pixel_path_1 = convert_path_to_pixels(path_1)
    pixel_path_4 = convert_path_to_pixels(path_4)

    """Setting up the streams for all vision sensor images"""
    sim.simxGetVisionSensorImage(client_id, vision_sensor_1, 0, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(client_id, vision_sensor_4, 0, sim.simx_opmode_streaming)
    sim.simxGetVisionSensorImage(client_id, vision_sensor_5, 0, sim.simx_opmode_streaming)

    """Retrieving vision sensor images"""
    vision_sensor_image_1, image_resolution_1, return_code = task_2a.get_vision_sensor_image(
        vision_sensor_1)
    vision_sensor_image_4, image_resolution_4, return_code = task_2a.get_vision_sensor_image(
        vision_sensor_4)

    """#Transforming image"""
    transformed_image_1 = task_2a.transform_vision_sensor_image(
        vision_sensor_image_1, image_resolution_1)
    transformed_image_4 = task_2a.transform_vision_sensor_image(
        vision_sensor_image_4, image_resolution_4)

    """Warping transformed image"""
    warped_img_1 = task_1b.applyPerspectiveTransform(transformed_image_1)
    warped_img_4 = task_1b.applyPerspectiveTransform(transformed_image_4)

    """Extracting ball positions from image"""
    shapes_1 = task_1a_part1.scan_image(warped_img_1)
    shapes_4 = task_1a_part1.scan_image(warped_img_4)

    cx_4 = 0
    cy_4 = 0

    flag = True
    f4 = False
    f5 = True
    while(flag):

        vision_sensor_image_1, image_resolution_1, return_code = task_2a.get_vision_sensor_image(
            vision_sensor_1)
        vision_sensor_image_4, image_resolution_4, return_code = task_2a.get_vision_sensor_image(
            vision_sensor_4)
        vision_sensor_image_5, image_resolution_5, return_code = task_2a.get_vision_sensor_image(
            vision_sensor_5)

        """#Transforming image"""
        transformed_image_1 = task_2a.transform_vision_sensor_image(
            vision_sensor_image_1, image_resolution_1)
        transformed_image_4 = task_2a.transform_vision_sensor_image(
            vision_sensor_image_4, image_resolution_4)
        transformed_image_5 = task_2a.transform_vision_sensor_image(
            vision_sensor_image_5, image_resolution_5)

        """Warping transformed image"""
        warped_img_1 = task_1b.applyPerspectiveTransform(transformed_image_1)
        warped_img_4 = task_1b.applyPerspectiveTransform(transformed_image_4)

        """Extracting ball positions from image"""
        shapes_1 = task_1a_part1.scan_image(warped_img_1)
        shapes_4 = task_1a_part1.scan_image(warped_img_4)
        shapes_5 = task_1a_part1.scan_image(transformed_image_5)

        if(len(shapes_5['Circle']) != 0 and f5 == True):
            send_data_to_draw_path(client_id, path_4, 4)
            f5 = False

        if(len(shapes_4['Circle']) != 0 and f4 == False):

            cx_4 = shapes_4['Circle'][1]
            cy_4 = shapes_4['Circle'][2]
            check_x1 = abs(cx_4 - (t4_end[1] * 80))
            check_y1 = abs(cy_4 - (t4_end[0] * 80))

            init = 0
            task_3.change_setpoint([500, -100])

            while(init < 5):

                task_3.control_logic(400, 0, 0)
                init += 1

            j = 1
            destination_cell = [pixel_path_4[len(pixel_path_4)-1][1], pixel_path_4[len(pixel_path_4)-1][0]]

            while not(check_x1 <= 40 and check_y1 <= 40) and j < len(pixel_path_4):

                next = [pixel_path_4[j][1], pixel_path_4[j][0]]

                if next != destination_cell:
                    while (next[0] == pixel_path_4[j-1][1] and next[0] == pixel_path_4[j+1][1]) or (next[1] == pixel_path_4[j-1][0] and next[1] == pixel_path_4[j+1][0]):

                        j += 1
                        next = [pixel_path_4[j][1], pixel_path_4[j][0]]

                        if next == destination_cell:
                            break
                
                if(j >= len(pixel_path_4) - 1):
                        # nextsetpt[0] = 800
                        next[0] = 800
                task_3.change_setpoint(next)
                
                check_x2 = abs(cx_4 - next[0])
                check_y2 = abs(cy_4 - next[1])

                while not(check_x2 <= 20 and check_y2 <= 20):

                    vision_sensor_image_4, image_resolution_4, return_code = task_2a.get_vision_sensor_image(
                        vision_sensor_4)
                    """#Transforming image"""
                    transformed_image_4 = task_2a.transform_vision_sensor_image(
                        vision_sensor_image_4, image_resolution_4)
                    """Warping transformed image"""
                    warped_img_4 = task_1b.applyPerspectiveTransform(
                        transformed_image_4)

                    """Extracting ball positions from image"""
                    shapes_4 = task_1a_part1.scan_image(warped_img_4)

                    # nextsetpt = [pixel_path_4[j][1], pixel_path_4[j][0]]

                    

                    # task_3.change_setpoint(nextsetpt)
                    cx_4 = shapes_4['Circle'][1]
                    cy_4 = shapes_4['Circle'][2]
                    task_3.control_logic(cx_4, cy_4, 0)
                    check_x2 = abs(cx_4 - next[0])
                    check_y2 = abs(cy_4 - next[1])

                j += 1
            f4 = True

        if(len(shapes_1['Circle']) != 0):
            cx_1 = shapes_1['Circle'][1]
            cy_1 = shapes_1['Circle'][2]
            check_x1 = abs(cx_1 - (t1_end[1] * 80))
            check_y1 = abs(cy_1 - (t1_end[0] * 80))

            init = 0
            task_3.change_setpoint([-100, 0])

            while(init < 10):

                task_3.control_logic(0, 0, 1)
                init += 1

            j = 1
            destination_cell = [pixel_path_1[len(pixel_path_1)-1][1], pixel_path_1[len(pixel_path_1)-1][0]]

            while not(check_x1 <= 40 and check_y1 <= 40) and j < len(pixel_path_1):

                next = [pixel_path_1[j][1], pixel_path_1[j][0]]

                if next != destination_cell:
                    while (next[0] == pixel_path_1[j-1][1] and next[0] == pixel_path_1[j+1][1]) or (next[1] == pixel_path_1[j-1][0] and next[1] == pixel_path_1[j+1][0]):

                        j += 1
                        next = [pixel_path_1[j][1], pixel_path_1[j][0]]

                        if next == destination_cell:
                            break

                task_3.change_setpoint(next)

                check_x2 = abs(cx_1 - next[0])
                check_y2 = abs(cy_1 - next[1])

                while not(check_x2 <= 20 and check_y2 <= 20):

                    vision_sensor_image_1, image_resolution_1, return_code = task_2a.get_vision_sensor_image(
                        vision_sensor_1)
                    """#Transforming image"""
                    transformed_image_1 = task_2a.transform_vision_sensor_image(
                        vision_sensor_image_1, image_resolution_1)
                    """Warping transformed image"""
                    warped_img_1 = task_1b.applyPerspectiveTransform(
                        transformed_image_1)

                    """Extracting ball positions from image"""
                    shapes_1 = task_1a_part1.scan_image(warped_img_1)

                    #nextsetpt = [pixel_path_1[j][1], pixel_path_1[j][0]]

                    if(j == len(pixel_path_1) - 1):
                        #nextsetpt[0] = 800
                        next[0] = 800

                    # task_3.change_setpoint(nextsetpt)
                    cx_1 = shapes_1['Circle'][1]
                    cy_1 = shapes_1['Circle'][2]
                    task_3.control_logic(cx_1, cy_1, 1)
                    check_x2 = abs(cx_1 - next[0])
                    check_y2 = abs(cy_1 - next[1])

                j += 1

    task_2a.stop_simulation()

    ##################################################


# Function Name:    main (built in)
#        Inputs:    None
#       Outputs:    None
#       Purpose:    To call the main(rec_client_id) function written by teams when they
#					run task_5.py only.

# NOTE: Write your solution ONLY in the space provided in the above functions. This function should not be edited.
if __name__ == "__main__":

    client_id = task_2a.init_remote_api_server()
    main(client_id)
