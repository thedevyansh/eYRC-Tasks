'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Author List:		[ Shikhhar Siingh, Devyansh Chawla, Hardik Sharma]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv, split_into_cells, edge_values
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

#Function for splitting our image into cells
def split_into_cells(img):
	rows = np.vsplit(img, 10) #Vertical split into 10 rows
	cells = [] #array of boxes
	
	for r in rows:
		cols = np.hsplit(r, 10) #Horizontal split into 10 columns
		for cell in cols:
			cells.append(cell) #Storing each box
			
	return cells

#Function to get the values for each cell
def edge_values(img):
	y = img.shape[0] #height of the image
	x = img.shape[1] #width of the image
	
	B_left, G_left, R_left = (img[int(y / 2), 8]) #BGR of the left mid_point	
	B_top, G_top, R_top = (img[2, int(x / 2)]) #BGR of top mid_point
	B_right, G_right, R_right = (img[int(y / 2), x - 2]) #BGR of right mid_point
	B_bottom, G_bottom, R_bottom = (img[y - 2, int(x / 2)]) #BGR of bottom_midpoint
	
	value = 0 #Initialization of cell value 
	
	#Conditions to check if the pixel is black or not
	if B_left < 150 and G_left <150 and R_left<150:
		value = value + 2**0

	if B_top < 150 and G_top <150 and R_top<150:
		value = value + 2**1
	
	if B_right < 150 and G_right <150 and R_right<150:
		value = value + 2**2

	if B_bottom < 150 and G_bottom <150 and R_bottom<150:
		value = value + 2**3
		
	return value


##############################################################


def applyPerspectiveTransform(input_img):

	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

	warped_img = None
	
	img = input_img

	##############	ADD YOUR CODE HERE	##############

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
	
	#Finding Contours
	contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2. CHAIN_APPROX_NONE)

	areas = [] #list for storing areas of detected contours

	#Storing Contours
	for cnts in contours:
		area = cv2.contourArea(cnts)
		areas.append(area)
	
	max_area = np.amax(areas) #Finding the contour with maximum area
	
	
	#Processing contours
	for cnts in contours:
		
		if cv2.contourArea(cnts) == max_area:
			
			approx = cv2.approxPolyDP(cnts, 0.01 * cv2.arcLength(cnts, True), True) #Getting the approximate coordinates of the vertices of the contours
			# print(approx)

	points = approx.ravel() #Flattening the approx matrix 
	x = np.array([points[0],points[2],points[4],points[6]]) #Extracting x coordinates
	y = np.array([points[1],points[3],points[5],points[7]]) #Extracting y coordinates
	
	ratio = x[0] / x[1]
	
	if ratio >= 0.9 and ratio <=1.1 or x[0] - x[1] < 300:
		x = np.array([points[6],points[0],points[2],points[4]]) #Extracting x coordinates
		y = np.array([points[7],points[1],points[3],points[5]]) #Extracting y coordinates

	side = 1000 #warped_img size
	pts1 = np.float32([[x[1], y[1]],[x[0], y[0]],[x[2], y[2]],[x[3], y[3]]]) #Making points matrix for input image
	pts2 = np.float32([[0, 0], [side, 0], [0, side], [side, side]]) #Making points matrix for output image
	matrix = cv2.getPerspectiveTransform(pts1, pts2) #Getting perspective transform
	warped_img = cv2.warpPerspective(img, matrix, (side, side)) #Applying warp perspective
	##################################################

	return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""

	maze_array = []

	##############	ADD YOUR CODE HERE	##############
	
	cells = split_into_cells(warped_img) #Splitting the warped image into cells

	for i in range(10): #For each row
		rows = [] #Intializing row array
		for j in range(10): #For each column
			x =  edge_values(cells[i*10 + j]) #Getting the cell value
			rows.append(x) #Storing cell value in the row
		maze_array.append(rows)
	
	##################################################

	return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""
	
	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)
					
					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')