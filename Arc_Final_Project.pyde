import random

add_library('minim')
minim=Minim(this)

# Delcaring needed variables here

#States where the game is not supposed to be running
gameNotRunningStates = ['statsScreen', 'endScreen', 'minigameOneScreenOne', 'minigameOneScreenTwo', 
                         'minigameTwoScreenOne', 'minigameTwoScreenTwo', 'instructionMenu', 'startMenu']

#Image dictionary that stores the array indice in a dictionary
image_dict = {"arctitle" : 0,
              "backgroundone" : 1,
              "backgroundtwo" : 2,
              "backgroundthree" : 3,
              "backgroundfour" : 4,
              "backgroundfive" : 5,
              "backgroundmountain" : 6,
              "titleplay" : 7,
              "titleinstructions" : 8,
              "instructionsmenu" : 9,
              "titlenext" : 10,
              "spritestanding" : 11,
              "spriteup" : 12,
              "spritedown" : 13,
              "spriteleft" : 14,
              "spriteright" : 15,
              "skeleton" : 16,
              "backgroundend" : 17,
              "dirt" : 18,
              "sword" : 19,
              "speed" : 20,
              "damage" : 21,
              "water" : 22,
              "endflag" : 23}

# Boundaries of the screen
boundaries = {
              "left_bound" : 0,
              "right_bound" : 1080,
              "up_bound" : 0,
              "bottom_bound" : 720
              }


# Player Information
player = {"player_x" : 5, 
          "player_y" : 5,
          "player_height" : 75,
          "player_width" : 75,
          
          "jumping" : False, 
          "gravity" : 10,
          "max_jump_height" : 10,
          "jump_origin_y" : 5,
          "grounded" : True,
          
          "jumping" : False,
          "jump_from_y" : 0,
          "max_jump_height" : 200,
          "grounded" : False,
          "velocity_y" : 15,
          "gravity_speed" : 10,
          "falling_speed" : 0,
          
          "health" : 100, 
          "velocity_x" : 10,
          "alive" : True,
          "facing_direction" : "left",
          "max_health" : 100,
          "lives" : 3,
          "damage_dealt" : 10,
          "spawned_in" : False,
          "attacking" : False
          }


#Spawn point of the player
spawn_point = {"levelOne": [600, 720],
                "levelTwo" : [300, 200]
                }


# Set the player spawnpoint to the level's spawn point
player["player_x"] = spawn_point["levelOne"][0]
player["player_y"] = spawn_point["levelOne"][1]


#Movement keys 
current_keys = {"a" : False, 
                "d" : False, 
                " " : False,
                "w" : False,
                "r" : False} 

#Storing each level as a series of 2D arrays containing x, y, width, height and environment type and storing each array in a 2D array associated with a key for the level
environment = {"levelOne" :
                   [
        [834, 36, 173, 123, "endflag"],        
        [0, 598, 1100, 200, "dirt"],
        [772, 434, 303, 163, "dirt"],
        [842, 361, 232, 142, "dirt"],
        [906, 208, 169, 186, "dirt"],
        [728, 164, 349, 112, "dirt"],
        [385, 148, 253, 107, "dirt"],
        [215, 228, 126, 45, "dirt"],
        [28, 348, 160, 30, "dirt"],
        [278, 440, 157, 49, "dirt"],
        [563, 436, 219, 54, "dirt"]
        ]
}

#Information about the powerups
powerups_types = ["speed", "damage"]

powerups = {"levelOne" :
        [
        [50, 50, 50, 50, random.choice(powerups_types)],
        [100, 100, 50, 50, random.choice(powerups_types)]
        ]
}

#All the enemy information stored as an x, y, width and height and alive status along with health
enemies = {"levelOne" : 
        [
    [600,700, 70, 70, True, 100],
    [900, 700, 70, 70, True, 100] 
    ], 
           "levelTwo" : [
    [1, 1, 1, 1, True, 100],
    [1, 1, 1, 1, True, 100]
    ]
}

def overlapping(q1, q2, w1, w2):
#######################################################################
# Function Name: overlapping
# Function Purpose: Checks if two retancular boundaries are overlapping
# Parameters: q1 holds coordinate data, q2 holds coordinate data, w1 holds coordinate data, w2 holds coordinate data
# Variables: None
# Return: True if overlapping, false if not
#######################################################################

    return max(q1, q2) <= min(w1, w2)

def rect_overlapping(x1, y1, length1, width1, x2, y2, length2, width2):
#######################################################################
# Function Name: rect_overlapping
# Function Purpose: It calls the overlapping function to determine if two rectangles are overlapping
# Parameters: x1, holds an int. y1, holds an int. length1 holds an int. width1 holds an int. x2 holds an int. y2 holds an int. length2 holds an int. width2 holds an int
# Variables: None
# Return: True if overlapping, False is not
#######################################################################
    if (overlapping(x1, x1 + length1, x2, x2 + length2) and overlapping(y1, y1 + width1, y2, y2 + width2)):
        return True
    else:
        return False
           
def calculateCoordinates(current_level):
#######################################################################
# Function Name: calculateCoordinates
# Function Purpose: Callculates the valid coordinates of the player at any given point given the environment and current keys
# Parameters: current_level holds the current level data
# Variables: arr is used to hold the current environment data from the current level, platforms is this array but only those with the the tag platform
# Return: Nothing
#######################################################################
    global player, boundaries, enemies, spawnpoint, powerups, environment, current_keys
  
    arr = environment[current_level]
    
    platforms = platform_parser(arr)
    # print(platforms)
    # 1. spawn player in if spawned in not true
    if player["spawned_in"] == False:
        player["player_x"] = spawn_point[current_level][0]
        player["player_y"] = spawn_point[current_level][1]
        player["spawned_in"] = True
    
    # 2. check current_keys for left right movement
    if current_keys["a"]:            
        player["player_x"] -= player["velocity_x"]
        player["facing_direction"] = "left"
    
    if current_keys["d"]:
        player["player_x"] += player["velocity_x"]
        player["facing_direction"] = "right"
    #3. check jumping
    if (current_keys["w"] or current_keys[" "]) and (player["grounded"] == True):
        player["jumping"] = True
    
    if player["grounded"] == True:
        player["falling_speed"] = 0
        player["jump_from_y"] = player["player_y"]
        player["grounded"] = False
    else:
        player["falling_speed"] = player["gravity_speed"]
        
    if player["jumping"]:
        if player["player_y"] <= ( player["jump_from_y"] - player["max_jump_height"] ):
            player["jumping"] = False
        else:
            player["player_y"] -= player["velocity_y"]
    else:
        player["player_y"] += player["falling_speed"]
        if player["player_y"] > boundaries["bottom_bound"] - player["player_height"]:
            player["player_y"] = boundaries["bottom_bound"] - player["player_height"]
            player["jumping"] = False
            player["grounded"] = True
        

    # 3. check boundaries to check if illegal movement
    
    #3a. check for top, left, right and bottom of screen
    if player["player_x"] < boundaries["left_bound"]:
        player["player_x"] = boundaries["left_bound"]
    elif player["player_x"] + player["player_width"] > boundaries["right_bound"]:
        player["player_x"] = boundaries["right_bound"] - player["player_width"]

    if player["player_y"] < boundaries["up_bound"]:
        player["player_y"] = boundaries["up_bound"]
    elif player["player_y"] + player["player_height"] > boundaries["bottom_bound"]:
        player["player_y"] = boundaries["bottom_bound"] - player["player_height"]

    #3b.
    for i in range(len(platforms)):
        dirt_boundaries(platforms[i][0], platforms[i][1], platforms[i][2], platforms[i][3])

def dirt_boundaries(dirtx,dirty,dirtw,dirth):
#######################################################################
# Function Name: dirt_boundaries
# Function Purpose: the function is creating boundaries for a platform called dirt
# Parameters: the dimensions and top left corner of the dirt is passed in
# Variables: player is a variable as it is updated so taht no illegal movement happens
# Return: None
#######################################################################
    global player
    if player["jumping"] == False: 
        if (dirty < player["player_y"] + player["player_height"] < dirty+dirth and player["player_x"] < dirtx + dirtw and player["player_x"] + player["player_width"] > dirtx):
            player["player_y"] = dirty-dirth
            
    elif player["jumping"]:
        if dirty < player["player_y"] <= dirty + dirth and player["player_x"] < dirtx + dirtw and player["player_x"] + player["player_width"] > dirtx:
            player["jumping"] = False
            player["player_y"] = dirty+dirth
    
    if player["player_x"] < dirtx + dirtw and player["player_x"] + player["player_width"] > dirtx and player["player_y"] < dirty + dirth and player["player_y"] + player["player_height"] > dirty:
         if player["facing_direction"] == "left":
            player["player_x"] = dirtx+dirtw
         elif player["facing_direction"] == "right":
            player["player_x"] = dirtx-player["player_width"]    
       
    if dirtx < player["player_x"] + player["player_width"] and player["player_x"] < dirtx + dirtw and player["player_y"] + player["player_height"] > dirty - 6  and player["player_y"] < dirty + dirth:
        player["grounded"] = True
        
def platform_parser(arr):
#######################################################################
# Function Name: platform_parser
# Function Purpose: takes in an array of all the environment boundaries and returns only the dirt platforms
# Parameters: arr which holds a 3D array of all environment objects
# Variables: new_arr holds the new array of platforms
# Return: returns only the dirt platforms
#######################################################################
    new_arr = []
    for i in range(len(arr)):
        if arr[i][4] == "dirt":
            new_arr.append(arr[i])
    return new_arr

def water_parser(arr):
#######################################################################
# Function Name: water_parser
# Function Purpose: takes in an array of all the environment boundaries and returns only the water areas
# Parameters: arr which holds a 3D array of all environment objects
# Variables: new_arr holds the new array of waters
# Return: returns only the water areas
#######################################################################
    new_arr = []
    for i in range(len(arr)):
        if arr[i][4] == "water":
            new_arr.append(arr[i])
    return new_arr
            
def drawLevel(player, enemies, powerups, environment, background_picture):
#######################################################################
# Function Name: draw_level
# Function Purpose: takes in all relevent level variables and draws them on the screen
# Parameters: player (player data), enemies (enemy data), powerups (powerup data), environment (environnment data), background_picture(holds the current background picture)
# Variables: None
# Return: None
#######################################################################
    #draw background
    imageMode(CORNER)
    image(background_picture, 0, 0, 1080, 720)
    
    player_display_health()
    enemy_display_health(enemies)
    
    health_proccesing(environment, enemies)
    
    # draw player
    if player["alive"] == True and player["spawned_in"] == True:
        image(imageList[image_dict["spritestanding"]], player["player_x"], player["player_y"], player["player_width"], player["player_height"])
        
        if player["facing_direction"] == "left":
            image(imageList[image_dict["spriteleft"]], player["player_x"], player["player_y"], player["player_width"], player["player_height"])
        if player["facing_direction"] == "right":
            image(imageList[image_dict["spriteright"]], player["player_x"], player["player_y"], player["player_width"], player["player_height"])
            
        if player["attacking"] == True:
            if player["facing_direction"] == "left":
                image(imageList[image_dict["sword"]], player["player_x"] - player["player_width"], player["player_y"] + 30, 100, 100)
            if player["facing_direction"] == "right":
                image(imageList[image_dict["sword"]], player["player_x"] + player["player_width"], player["player_y"] + 30, 100, 100)
        
    # draw enemies
    for i in range(len(enemies)):
        if enemies[i][4] == True:
            image(imageList[image_dict["skeleton"]], enemies[i][0], enemies[i][1], enemies[i][2], enemies[i][3])
    
    # draw platforms
    
    valid_environment = ["dirt", "endflag", "water"]
    for i in range(len(environment)):
        for j in range(len(valid_environment)):
            if environment[i][4] == valid_environment[j]:
                image(imageList[image_dict[valid_environment[j]]], environment[i][0], environment[i][1], environment[i][2], environment[i][3])

    #draw powerups
    valid_powerups = ["speed", "damage"]    
    for i in range(len(powerups)):
        for j in range(len(valid_powerups)):
            if powerups[i][4] == valid_powerups[j]:
                image(imageList[image_dict[valid_powerups[j]]], powerups[i][0], powerups[i][1], powerups[i][2], powerups[i][3])

def nextLevel(current_level):

#######################################################################
# Function Name: nextLevel
# Function Purpose: takes in the current level and updates it to the next level
# Parameters: Takes in the current level
# Variables: gameStates which holds all possible valid game states
# Return: None
#######################################################################
    global gameState
    gameStates = ["gameLevelOne", "gameLevelTwo", "minigameOne" "gameLevelThree", "gameLevelFour", "minigameTwo", "gameLevelFive"]
    
    for i in range(len(gameStates)):
        if gameStates[i] == gameState:
            gameState = gameStates[i + 1]

def startMenu():
#######################################################################
# Function Name: startMenu
# Function Purpose: draw the start menu appropriately
# Parameters:None
# Variables: None
# Return: None
#######################################################################
    global areaPressed, gameState
    imageMode(CORNERS)
    rectMode(CORNERS)
    image(imageList[image_dict["backgroundone"]], 0, 0, 1080, 720)
    
    imageMode(CENTER)
    rectMode(CENTER)
    fill(255)
    rect(540,180, 270,150)
    image(imageList[image_dict["arctitle"]], 540, 180, 270, 180)
    
    rect(540, 400, 170, 130)
    image(imageList[image_dict["titleplay"]], 540, 400, 170, 140)
    
    rect(540, 600, 170, 130)
    image(imageList[image_dict["titleinstructions"]], 540, 600, 170, 140)

    if areaPressed == 0:
        gameState = 'gameLevelOne'
        areaPressed = None
        # print(gameState)
    elif areaPressed == 1:
        gameState = 'instructionMenu'
        areaPressed = None
        # print(gameState)
    
def instructionMenu():
#######################################################################
# Function Name: instructionMenu
# Function Purpose: draw the instruction menu appropriately
# Parameters:None
# Variables: None
# Return: None
#######################################################################
    global areaPressed, gameState
    rectMode(CORNERS)
    rect(0,0, 20000, 20000)
    
    imageMode(CORNERS)
    image(imageList[image_dict["instructionsmenu"]], 0, 0, 1080, 720)
    
    imageMode(CENTER)
    rectMode(CENTER)
    rect(950, 620, 230, 120)
    image(imageList[image_dict["titlenext"]], 950, 620, 270, 180)
    
    if areaPressed == 0:
        gameState = 'gameLevelOne'
        areaPressed = None
        # print(gameState)
    

def mouseInArea(arr, mousex, mousey):
#######################################################################
# Function Name: mouseInArea
# Function Purpose: check if the current mouse x and y is contained within a certain boundary
# Variables: None
# Return: True if it is contained, false if not
#######################################################################
    # print(arr)
    if mousex in range(arr[0][0], arr[1][0]):
        if mousey in range(arr[0][1], arr[1][1]):
            return True
    return False

def health_proccesing(environment, enemies):
#######################################################################
# Function Name: health_proccesing
# Function Purpose: update the player's health if colision with enemy or environment
# Variables: None
# Return: None
#######################################################################   
    global player
    
    water_areas = water_parser(environment)
    if player["health"] > -1:
        for i in range(len(water_areas)):
            if rect_overlapping(player["player_x"], player["player_y"], player["player_width"], player["player_height"], water_areas[i][0], water_areas[i][1], water_areas[i][2], water_areas[i][3]):
                player["health"] -= 1                                                                                    
        
        # for i in range(len(enemies)):
        #     if rect_overlapping(player["player_x"], player["player_y"], player["player_width"], player["player_height"], enemies[i][0], enemies[i][1], enemies[i][2], enemies[i][3]):
        #         player["health"] -= 1
            
    if player["health"] < 0 and player["alive"] == True:
        
        player["health"] = player["max_health"]
        player["lives"] -= 1
    
    if player["lives"] < 1:
        player["alive"] = False
    

def enemy_display_health(current_enemies):
#######################################################################
# Function Name: enemy_display_health
# Function Purpose: takes in all of the enemy's health information and displays it
# Variables: None
# Return: None
#######################################################################   
    rectMode(CENTER)

    for i in range(len(current_enemies)):
        
        fill(255, 0, 0)
        rect( (current_enemies[i][0] + (current_enemies[i][2]/2)), current_enemies[i][1] - 25, current_enemies[i][5], 10 )
    
    
def player_display_health():
#######################################################################
# Function Name: player_display_health
# Function Purpose: display's the player's health
# Variables: None
# Return: None
#######################################################################   
    global player
    
    if player["alive"] == False:
        text("Press R to Respawn", player["player_x"] - 10, player["player_y"] - 10)
        
    if current_keys["r"] == True:
        if player["alive"] == False and player["lives"] > 1:
            player["alive"] = True
    
    
    if player["health"] < 1:
        return
    if player["alive"] == False:
        return
    
    rectMode(CORNER)
    
    fill(0)
    rect( player["player_x"] - 20, player["player_y"] - 28, player["max_health"], 10)
    
    rectMode(CORNER)
    
    fill(255, 0, 0)
    rect( player["player_x"] - 20, player["player_y"] - 28, player["health"], 10)
    
    textSize(20)
    textMode(CENTER)

    text("Lives: " + str(player["lives"]),  player["player_x"] + (player["player_width"]/2) - 35, player["player_y"] - 45)

def startmusic():
#######################################################################
# Function Name: startmusic
# Function Purpose: start the game's music
# Variables: None
# Return: None
#######################################################################   
    minim = Minim(this)
    songstart = minim.loadFile("startMusic.mp3")
    songstart.play()
    songstart.loop() 

def loadImageNames():
#######################################################################
# Function Name: loadImageNames
# Function Purpose: read all the image names from a .txt file
# Variables: rowList which contains the picture names
# Return: rowList which is of all the player names
#######################################################################   
    file = open("images.txt")
    fileList = []          
    text = file.readlines()
     
    for line in text:
        line = line.strip() 
        row = ""
        for j in line:
            row = row + j
        rowList = row.split(",")
        
    file.close
    
    return (rowList)

def loadImages(imageListNames):
#######################################################################
# Function Name: loadImages
# Function Purpose: load all of the pngs into proccesing
# Variables: numimages which is number of images
# Return: an array of all the memory locations of the pngs
#######################################################################   
    numImages = len(imageListNames)
    imageList = ["" for i in range(numImages)]
    
    for i in range(numImages):
        imageList[i] = loadImage(imageListNames[i])

    return(imageList)

def setup():
    global gameState, areaPressed, imageList
    startmusic()
    playerCoords = [400, 400]
    
    areaPressed = None
    gameState = 'startMenu'
    
    size(1080,720)
    
    imageListNames = loadImageNames()
    imageList = loadImages(imageListNames)
    
def draw():
    global gameState, areaPressed
    
    if gameState == 'startMenu':
        startMenu()
        
    if gameState == 'instructionMenu':
        instructionMenu()

    if gameState == 'gameLevelOne':
        imageMode(CORNER)
        calculateCoordinates("levelOne")
        drawLevel(player, enemies["levelOne"], powerups["levelOne"], environment["levelOne"], imageList[4])
 
        
    if gameState == 'statsScreen':
        pass
    if gameState == 'endScreen':
        pass
 


def mousePressed():
    global areaPressed, player, activeAreas
    
    activeAreas = []
    areaPressed = None
    
    if gameState == 'startMenu':
        activeAreas = [
                       [ [455, 336], [625, 467] ],
                       [ [456, 539], [624, 665] ]
                       ]
    
    if gameState == 'instructionMenu':
        activeAreas = [
                       [ [838, 561], [1064, 678] ]
                       ]
    if gameState in ["gameLevelOne", "gameLevelTwo", "gameLevelThree", "gameLevelFour", "gameLevelFive"]:
        player["attacking"] = True

        
    # if gameState == 'gameLevelOne':
    #     activeAreas = [
    #                    [ [ [541, 331], [604, 384] ]
    #                     ]
    
    # if gameState == 'gameLevelTwo':
    #     activeArea= [
    #                  [ [    ],   [     ] ]
    #                  ]
        
    # if gameState == 'gameLevelThree':
    #     activeArea= [
    #         [ [    ],   [     ] ]
    #         ]
    # if gameState == 'gameLevelFour':
    #     activeArea= [
    #         [ [    ],   [     ] ]
    #         ]
    # if gameState == 'gameLevelFive':
    #     activeArea= [
    #         [ [    ],   [     ] ]
    #         ]
        
    # if gameState == 'minigameOne':
    #     activeArea= [
    #                  [ [    ],   [     ] ]
    #                  ]
        
    # if gameState == 'minigameTwo':
    
    for i in range(len(activeAreas)):
        if mouseInArea(activeAreas[i], mouseX, mouseY):
            areaPressed = i
        
    # if mouseButton == CENTER:
    #     println([mouseX, mouseY])

           
              
def keyPressed():
    global gameState, current_keys
    
    currentKey = None
   
    
    if not gameState in gameNotRunningStates:
        currentKey = key
        current_keys[currentKey] = True

def keyReleased():
    global gameState, current_keys, player
    if not gameState in gameNotRunningStates:
        currentKey = key
        current_keys[currentKey] = False
        
        player["attacking"] = False
        
