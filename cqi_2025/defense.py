
wasLastPlacedX = False
def defenseMode(color_dict):
    print("defence")
    if True: #if its our turn to place block
        blockCoordinate =placeBlock()
        #call place block
    
    
def placeBlock():

    #some way to get the data from the json      
    playerX = 0
    playerY = 0
    if not wasLastPlacedX:
        return [playerX+1,playerY]
    else:
        return [playerX,playerY+1]
    
    
def fuckGreenBlock(map):
    print("fucking greens")        