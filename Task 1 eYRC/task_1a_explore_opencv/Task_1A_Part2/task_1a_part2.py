'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 2 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID:			[ NB_2650 ]
# Author List:		[ Shikhhar Siingh ]
# Filename:			task_1a_part2.py
# Functions:		process_video, update_dictionary
# 					[ Comma separated list of functions in this file ]
# Global variables:	frame_details
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


# Global variable for details of frames seleced in the video will be put in this dictionary, returned from process_video function
frame_details = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

#Function for updating dictionary
def update_dictionary(frame_no, cx, cy):
	global frame_details
	arr = [cx, cy]
	frame_details.update({frame_no: arr})

##############################################################


def process_video(vid_file_path, frame_list):

	"""
	Purpose:
	---
	this function takes file path of a video and list of frame numbers as arguments
	and returns dictionary containing details of red color circle co-ordinates in the frame

	Input Arguments:
	---
	`vid_file_path` :		[ str ]
		file path of video
	`frame_list` :			[ list ]
		list of frame numbers

	Returns:
	---
	`frame_details` :		[ dictionary ]
		co-ordinate details of red colored circle present in selected frame(s) of video
		{ frame_number : [cX, cY] }

	Example call:
	---
	frame_details = process_video(vid_file_path, frame_list)
	"""

	global frame_details
	
	##############	ADD YOUR CODE HERE	##############
	
	#Preprocessing
	frame_details.clear() #Clearing the output dictionary 
	frame_list = np.sort(frame_list) #Sorting the frame_list to address jumbled frame number entries
	
	# print(frame_list)
	
	frame = cv2.VideoCapture(vid_file_path) #Video capturing from the source

	count = 0 #frame counter
	success = 1 #frame extraction success  
	i = 0 #frame_list item counter
	while success:
		success, img = frame.read() #Reading frame
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Converting the frame to HSV
		
		#Masking for specific hues of red
		lower_red = np.array([0, 190, 180]) #Lower HSV red range
		upper_red = np.array([10, 255, 255]) #Upper HSV Red Range
		mask = cv2.inRange(hsv, lower_red, upper_red) #Applying mask on the frams
		
		contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #Finding contours in the masked frame
		
		for cnts in contours:
			area = cv2.contourArea(cnts) #calculating areas of all found contours
			
			#Processing to occur only if area > 1000 (to address noise contours)
			if area > 1000:
				
				#cv2.drawContours(img, cnts, -1, (0, 255, 0), 10)
				x, y, w, h = cv2.boundingRect(cnts) #Finding the bounding rectangle of the contour
				
				cx = int((x + x + w)/2) #Average x coordinate givey x coordinate of centroid
				cy = int((y + y + h)/2) #Average y coordinate gives y coordinate of centroid
				
				count += 1 #frame counter increment
				
				#Checks if the current frame matches the frame_list element
				if count == frame_list[i]:
					update_dictionary(frame_list[i], cx, cy) #Dictionary updation
					i += 1 #frame_list array counter increment
		
		if count > 403 or i == len(frame_list): #Condition to address out of bound processing and End of video error
			break

	

	##################################################

	return frame_details


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes input for selecting one of two videos available in Videos folder
#                   and a input list of frame numbers for which the details are to be calculated. It runs process_video
#                   function on these two inputs as argument.

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	print('Currently working in '+ curr_dir_path)

	# path directory of videos in 'Videos' folder
	vid_dir_path = curr_dir_path + '/Videos/'
	
	try:
		file_count = len(os.listdir(vid_dir_path))
	
	except Exception:
		print('\n[ERROR] "Videos" folder is not found in current directory.')
		exit()
	
	print('\n============================================')
	print('\nSelect the video to process from the options given below:')
	print('\nFor processing ballmotion.m4v from Videos folder, enter \t=> 1')
	print('\nFor processing ballmotionwhite.m4v from Videos folder, enter \t=> 2')
	
	choice = input('\n==> "1" or "2": ')

	if choice == '1':
		vid_name = 'ballmotion.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotion.m4v')
	
	elif choice=='2':
		vid_name = 'ballmotionwhite.m4v'
		vid_file_path = vid_dir_path + vid_name
		print('\n\tSelected video is: ballmotionwhite.m4v')
	
	else:
		print('\n[ERROR] You did not select from available options!')
		exit()
	
	print('\n============================================')

	if os.path.exists(vid_file_path):
		print('\nFound ' + vid_name)
	
	else:
		print('\n[ERROR] ' + vid_name + ' file is not found. Make sure "Videos" folders has the selected file.')
		exit()
	
	print('\n============================================')

	print('\nEnter list of frame(s) you want to process, (between 1 and 404) (without space & separated by comma) (for example: 33,44,95)')

	frame_list = input('\nEnter list ==> ')
	frame_list = list(frame_list.split(','))

	try:
		for i in range(len(frame_list)):
			frame_list[i] = int(frame_list[i])
		print('\n\tSelected frame(s) is/are: ', frame_list)
	
	except Exception:
		print('\n[ERROR] Enter list of frame(s) correctly')
		exit()
	
	print('\n============================================')

	try:
		print('\nRunning process_video function on', vid_name, 'for frame following frame(s):', frame_list)
		frame_details = process_video(vid_file_path, frame_list)

		if type(frame_details) is dict:
			print(frame_details)
			print('\nOutput generated. Please verify')
		
		else:
			print('\n[ERROR] process_video function returned a ' + str(type(frame_details)) + ' instead of a dictionary.\n')
			exit()
	
	except Exception:
		print('\n[ERROR] process_video function is throwing an error. Please debug process_video function')
		exit()

	print('\n============================================')

