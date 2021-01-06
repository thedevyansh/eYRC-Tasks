--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b_lua
# Functions:        [ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

base_children_list={} --Do not change or delete this variable
baseHandle = -1       --Do not change or delete this variable
--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION
**************************************************************
	Function Name : createWall()
	Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
	
	returns the object handle of the wall created
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
	wallObjectHandle = sim.createPureShape(0, 8, {0.09, 0.01, 0.1}, 0.0001, nil)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm to understand the parameters passed to this function
	sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
	sim.setObjectInt32Parameter(wallObjectHandle,sim.shapeintparam_respondable_mask,65280)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm#sim.setObjectInt32Parameter to understand the various parameters passed. 	
	--The walls should only be collidable with the ball and not with each other.
	--Hence we are enabling only the local respondable masks of the walls created.
	sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
	--Walls may have to be set as renderable........................... 
	--This is required to make the wall as collidable
	return wallObjectHandle
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
	Purpose:
	---
	Receives data via Remote API. This function is called by 
	simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	These 4 variables represent the data being passed from remote
	API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

	--*******************************************************
	--               ADD YOUR CODE HERE
		for i=1,10
		do 
		maze_array[i]={}
				for j=1,10
				do
				maze_array[i][j]=inInts[10*(i-1)+j]
				end
		end    
	--*******************************************************
	return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
	Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
		incr =0.1
		ypos=0.5
		zpos=0.085
		local k=1
		while k<=11
		do
		
		xpos=-0.45
				local i=1
				while i<=10
				do
						wallObjectHandle= createWall();
						baseHandle=sim.getObjectHandle('force_sensor_pw_1');
						sim.setObjectParent( wallObjectHandle,baseHandle,false);
						sim.setObjectPosition(wallObjectHandle,baseHandle,{xpos,ypos,zpos})
						sim.setObjectOrientation(wallObjectHandle,baseHandle,{0,0,0})
						sim.setObjectName(wallObjectHandle,string.format('HorizontalWall_%sX%s',i,k))
						xpos=xpos+incr
						i=i+1
				end
		ypos=ypos-incr
		k=k+1    
		end 
	--*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
	Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
		xpos=-0.5
		zpos=0.085
		incr=0.1
		local k=1
		while k<=11
		do
		ypos=0.45
				i=1
				while i<=10
				do
				
				wallObjectHandle= createWall();
				baseHandle=sim.getObjectHandle('force_sensor_pw_1');
				sim.setObjectParent( wallObjectHandle,baseHandle,false);
				sim.setObjectOrientation(wallObjectHandle,baseHandle,{0,0,77})
				sim.setObjectPosition(wallObjectHandle,baseHandle,{xpos,ypos,zpos})
				sim.setObjectName(wallObjectHandle,string.format('VerticalWall_%sX%s',k,i))
				ypos=ypos-incr
				i=i+1
				end
		xpos=xpos+incr
		k=k+1
		end
		
	--*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
	Purpose:
	---
	Deletes all the grouped walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
		i=0
		baseHandle=sim.getObjectHandle('force_sensor_pw_1')
		object=sim.getObjectChild(baseHandle,i)
		supportHandle=sim.getObjectHandle('Support') 
		while object~=-1
		do
				if object~=supportHandle then
					sim.removeObject(object)
				else 
						i=i+1
				end   
				object=sim.getObjectChild(baseHandle,i)
		end
	--*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
						  FUNCTION
**************************************************************
	Function Name : createMaze()
	Purpose:
	---
	Creates the maze in the given scene by deleting specific 
	horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
	
	--*******************************************************
	--               ADD YOUR CODE HERE
		y=1
		
	while y<=10
	do 
			x=1
			while x<=10
			do
			
			cell=maze_array[y][x]
				topWall= sim.getObjectHandle(string.format('HorizontalWall_%sX%s@silentError',x,y))
				
				bottomWall=sim.getObjectHandle(string.format('HorizontalWall_%sX%s@silentError',x,y+1))
				
				leftWall=sim.getObjectHandle(string.format('VerticalWall_%sX%s@silentError',x,y))
				
				rightWall= sim.getObjectHandle(string.format('VerticalWall_%sX%s@silentError',x+1,y))
				

			
			local num = 8
			
			while num ~= 0
			do
			
			if cell < num then
			if num == 8 and bottomWall ~= -1 then
			sim.removeObject(bottomWall)
			elseif num == 4 and rightWall ~= -1 then
			sim.removeObject(rightWall)
			elseif num == 2 and topWall ~= -1 then
			sim.removeObject(topWall)
			elseif num == 1 and leftWall ~= -1 then
			sim.removeObject(leftWall)
			end
			
			else
			cell = cell % num
			end
			
			num = num / 2
			end
			
			x=x+1
			end
			
		y=y+1  
	end
	--*******************************************************
end
--[[
	Function Name : groupWalls()
	Purpose:
	---
	Groups the various walls in the scene to one object.
	The name of the new grouped object should be set as 'walls_1'.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	groupWalls()
**************************************************************	
]]--

walls_1 = 0
function groupWalls()
	--*******************************************************
	--               ADD YOUR CODE HERE
	
	y = 1
	groupables = {}
	while y <= 10
	do
		x = 1
		while x <= 10
		do
			topWall= sim.getObjectHandle(string.format('HorizontalWall_%sX%s@silentError',x,y))
			
			bottomWall=sim.getObjectHandle(string.format('HorizontalWall_%sX%s@silentError',x,y+1))
			
			leftWall=sim.getObjectHandle(string.format('VerticalWall_%sX%s@silentError',x,y))
			
			rightWall= sim.getObjectHandle(string.format('VerticalWall_%sX%s@silentError',x+1,y))
			
			if topWall ~= -1 then
				table.insert(groupables, topWall)
			end
			if bottomWall ~= -1 then
				table.insert(groupables, bottomWall)
			end
			if leftWall ~= -1 then
			table.insert(groupables, leftWall)
			end
			if rightWall ~= -1 then
			table.insert(groupables, rightWall)
			end
		end
	end
		
	walls_1 = sim.groupShapes(groupables ,false)
	--*******************************************************
end


--[[
	Function Name : addToCollection()
	Purpose:
	---
	Adds the 'walls_1' grouped object to the collection 'colliding_objects'.  

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	addToCollection()
**************************************************************	
]]--

function addToCollection()
	--*******************************************************
	--               ADD YOUR CODE HERE
		colliding_objects = sim.getCollectionHandle("colliding_objects")
		sim.addToCollection(collect, walls_1, sim_handle_single, 0)
	--*******************************************************
end

--[[
	******************************************************************************
			YOU ARE ALLOWED TO MODIFY THIS FUNCTION DEPENDING ON YOUR PATH. 
	******************************************************************************
	Function Name : drawPath(inInts,path,inStrings,inBuffer)
	Purpose:
	---
	Builds blue coloured lines in the scene according to the
	path generated from the python file. 

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats (containing the path generated)
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function drawPath(inInts,path,inStrings,inBuffer)
	posTable=sim.getObjectPosition(wallsGroupHandle,-1)
	print('=========================================')
	print('Path received is as follows: ')
	print(path)
	if not lineContainer then
		_lineContainer=sim.addDrawingObject(sim.drawing_lines,1,0,wallsGroupHandle,99999,{0.2,0.2,1})
		sim.addDrawingObjectItem(_lineContainer,nil)
		if path then
			local pc=#path/2
			for i=1,pc-1,1 do
				lineDat={path[(i-1)*2+1],path[(i-1)*2+2],posTable[3]-0.03,path[(i)*2+1],path[(i)*2+2],posTable[3]-0.03}
				sim.addDrawingObjectItem(_lineContainer,lineDat)
			end
		end
	end
	return inInts, path, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : sysCall_init()
	Purpose:
	---
	Can be used for initialization of parameters
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
	--*******************************************************
	--               ADD YOUR CODE HERE
	--*******************************************************
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION.
		YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT 
		PARAMETERS ONLY FOR CREATEMAZE() FUNCTION
**************************************************************
	Function Name : sysCall_beforeSimulation()
	Purpose:
	---
	This is executed before simulation starts
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
	
	generateHorizontalWalls()
	generateVerticalWalls()
	createMaze()--You can define your own input and output parameters only for this function
	groupWalls()
	addToCollection()
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
	Purpose:
	---
	This is executed after simulation ends
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
	-- is executed after a simulation ends
	deleteWalls()
    evaluation_screen_respondable=sim.getObjectHandle('evaluation_screen_respondable@silentError')
    if(evaluation_screen_respondable~=-1) then
        sim.removeModel(evaluation_screen_respondable)
    end
end

function sysCall_cleanup()
	-- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details