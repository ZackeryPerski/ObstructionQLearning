import pygame
import numpy as np
from pygame.locals import *

pygame.init()
pygame.display.set_caption("OBSTRUCTION")
rng = np.random.default_rng()

C_NAVY = (0,0,128)
C_TAN = (210,180,140)
C_PINK = (255,180,180)
C_BLACK = (0,0,0)
C_RED = (255,0,0)
C_GREEN = (0,255,0)
C_BLUE = (0,0,255)
C_YELLOW = (200,200,0)
C_GOLD = (255,215,0)
C_WHITE = (255,255,255)
SCALE = 20

screen_width = 17*SCALE
screen_height = 17*SCALE
screen = pygame.display.set_mode((screen_width, screen_height))
gameboardVis = None

def initGameBoard():
    '''
        Visible Structure:
        -1 Inaccessible
        0 Standard space
        1-5 red players
        6-10 yellow players
        11-15 blue players
        16-20 green players
        21 obstructions
        22 finish
        23 red starter full
        24 red starter empty
        25 red starter square
        26 yellow starter full
        27 yellow starter empty
        28 yellow starter square
        29 blue starter full
        30 blue starter empty
        31 blue starter square
        32 green starter full
        33 green starter empty
        34 green starter square

    '''
    gameboardVis = np.zeros((17,17),dtype=int)
    for i in range(0,17): #initialize world space. Fill with walls.
        for j in range(0,17):
            gameboardVis[i][j]=-1
    #Mark finish line.
    gameboardVis[0][8]=22
    #top row near finish.
    for i in range(1,16):
        gameboardVis[1][i]=0
    #obstruction near finish.
    gameboardVis[1][8]=21
    #top of pyramid area
    for i in range(2,6):
        gameboardVis[i][1] = 0
        gameboardVis[i][15] = 0
    for i in range(2,5):
        gameboardVis[5][i]=0
        gameboardVis[5][16-i]=0
    for i in range(4,8):
        gameboardVis[4][i]=0
        gameboardVis[4][16-i]=0
    #Draw pyramid sans obstructions.
    for i in range(2,9,2):
        for j in range(0,i):
            gameboardVis[6+i-2][8+j+1]=0
            gameboardVis[6+i-2][8-j-1]=0
        gameboardVis[6+i-2][8]=0
        gameboardVis[6+i-1][8+i]=0
        gameboardVis[6+i-1][8-i]=0
    #column of obstructions
    for i in range(4,7):
        gameboardVis[i][8]=21
    #random starting obstruction spots
    gameboardVis[8][6]=21
    gameboardVis[8][10]=21
    for i in range(0,17,4):
        gameboardVis[12][i]=21
    #Row before start
    for i in range(0,17):
        gameboardVis[14][i]=0
    #Small row next to starts
    for i in range(7,10):
        gameboardVis[15][i]=0
    #odd missing connects
    gameboardVis[11][6]=0
    gameboardVis[11][10]=0
    gameboardVis[13][4]=0
    gameboardVis[13][8]=0
    gameboardVis[13][12]=0

    #red starter spots
    gameboardVis[15][1]=23 #pieces 1-5 starting spots
    gameboardVis[15][3]=23
    gameboardVis[16][1]=23
    gameboardVis[16][2]=23
    gameboardVis[16][3]=23
    gameboardVis[15][2]=25 #main starting spot

    #yellow starter spots
    gameboardVis[15][4]=26 #pieces 1-5 starting spots
    gameboardVis[15][6]=26
    gameboardVis[16][4]=26
    gameboardVis[16][5]=26
    gameboardVis[16][6]=26
    gameboardVis[15][5]=28 #main starting spot
    
    #blue starter spots
    gameboardVis[15][10]=29 #pieces 1-5 starting spots
    gameboardVis[15][12]=29
    gameboardVis[16][10]=29
    gameboardVis[16][11]=29
    gameboardVis[16][12]=29
    gameboardVis[15][11]=31 #main starting spot

    #green starter spots
    gameboardVis[15][13]=32 #pieces 1-5 starting spots
    gameboardVis[15][15]=32
    gameboardVis[16][13]=32
    gameboardVis[16][14]=32
    gameboardVis[16][15]=32
    gameboardVis[15][14]=34 #main starting spot
    return gameboardVis

def drawGameBoard():
    screen.fill(C_NAVY)
    rect=pygame.Rect(8*SCALE,0,SCALE,SCALE)
    pygame.draw.rect(screen,C_GOLD,rect,border_radius=1)
    pygame.draw.rect(screen,C_BLACK,rect,border_radius=1,width=1)            
    for i in range(1,17):
        for j in range(0,17):
            val = gameboardVis[i][j]
            if(val==-1):
                continue
            rect = pygame.Rect(j*SCALE,i*SCALE,SCALE,SCALE)
            if(val>=0 and val<=21):
                pygame.draw.rect(screen,C_TAN,rect,border_radius=1)
                pygame.draw.rect(screen,C_BLACK,rect,border_radius=1,width=1)
                if(val==21):#draw blocker
                    pygame.draw.circle(screen,C_BLACK,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.8))
                if(val>=1 and val<=5):#draw red player token
                    continue
                if(val>=6 and val<=10):#draw yellow player token
                    continue
                if(val>=11 and val<=15):#draw blue player token
                    continue
                if(val>=16 and val<=20):#draw green player token
                    continue
            else:#starter zones
                pygame.draw.rect(screen,C_WHITE,rect,border_radius=1)
                pygame.draw.rect(screen,C_BLACK,rect,border_radius=1,width=1)
                if(val==23):#red filled starter
                    pygame.draw.circle(screen,C_RED,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.8))
                elif(val==24):#red unfilled starter
                    pygame.draw.circle(screen,C_RED,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.6))
                elif(val==26):#yellow filled starter
                    pygame.draw.circle(screen,C_YELLOW,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.8))
                elif(val==27):#yellow unfilled starter
                    pygame.draw.circle(screen,C_YELLOW,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.6))
                elif(val==29):#blue filled starter
                    pygame.draw.circle(screen,C_BLUE,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.8))
                elif(val==30):#blue unfilled starter
                    pygame.draw.circle(screen,C_BLUE,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.6))
                elif(val==32):#green filled starter
                    pygame.draw.circle(screen,C_GREEN,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.8))
                elif(val==33):#green unfilled starter
                    pygame.draw.circle(screen,C_GREEN,center=(j*SCALE+int(SCALE/2),i*SCALE+int(SCALE/2)),radius=int(int(SCALE/2)*.6))
                else:#all starters share the same basic appearance
                    continue

def getPlayerPositions(player, visToLogMap):
    '''TODO:Need to finish out this logic as well. This is a dependency for several functions.'''
    positions = np.zeros(5,141)
    #numpy.where will likely be helpful here.

    return positions

def getValidMoves(activePlayer, movementVal, visToLogMap):
    '''TODO:Need to finish out the logic. Placeholdered for now.'''
    validMoves = np.zeros(5,141)
    return validMoves, True

def getObstructionSpaces(visToLogMap):
    obstructions = np.zeros(1,141)
    for i in range (1,15): #exclude top row and the bottom rows, as those are invalid positions.
        for j in range(0,17):
            if gameboardVis[i][j] == 21:
                obstructions[0][visToLogMap[(i,j)]]=1
    return obstructions

def retrieveGameState(activePlayer, movementVal, visToLogMap):
    '''
        Returns a 2d matrix that is more ML friendly that is one hot encoded.
        0 = red
        1 = yellow
        2 = blue
        3 = green
        Output of retrieve gamestate is based off of the active player, making it easier to train multiple colored agents.
        The encoded board is optimized by having only the valid spaces mapped, e.g. no walls are present.
    '''
    validMovesEncoded, validMovesExist = getValidMoves(activePlayer, movementVal, visToLogMap)
    if not validMovesExist: #INCREDIBLY RARELY if there are NO valid moves, your turn is straight up skipped. Sad.
        return None #will indicate to end turn prematurely before any actions are taken. 
    redPositions = getPlayerPositions(0,visToLogMap)
    yellowPositions = getPlayerPositions(1,visToLogMap)
    bluePositions = getPlayerPositions(2,visToLogMap)
    greenPositions = getPlayerPositions(3,visToLogMap)
    obstructions = getObstructionSpaces(visToLogMap)
    gameboardEncoded = np.vstack((validMovesEncoded,redPositions,yellowPositions,bluePositions,greenPositions,obstructions))

    return gameboardEncoded

def getLogicalMapping(gameboardVis):
    '''returns a dictionary of valid positions based off of (x,y) tuples mapped to a linear array.'''
    mapping = {}
    count = 0
    for i in range(0,17):
        for j in range(0,17):
            if gameboardVis[i][j] != 0:
                mapping[(i,j)] = count
                count = count+1
    return mapping


gameboardVis=initGameBoard()
visToLogMap = getLogicalMapping(gameboardVis)

drawGameBoard()
# Update the display
pygame.display.flip()

#playSpaces = 141 #as a reference.


running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


# Quit Pygame
pygame.quit()

