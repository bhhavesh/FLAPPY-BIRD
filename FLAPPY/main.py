import random
import sys
import pygame
from pygame. locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS ={}
PLAYER ='Gallery/sprites/Flappy.png'
BACKGROUND='Gallery/sprites/background.png'
PIPE='Gallery/sprites/pillar.png'
def WelcomeScreen():
    """
    Shows welcome image on the screen
    """
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2
    messagex=int(SCREENWIDTH-GAME_SPRITES['player'].get_height())/40
    messagey=int(SCREENHEIGHT*0.01)
    basex =0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
def mainGame():
    score = 0
    playerx = int (SCREENWIDTH/5)
    playery = int (SCREENWIDTH/2)
    basex = 0
    # create 2 pipes for blitting
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()
    
    #list  of upper pipes
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y': newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[0]['y']},
    ]
    #list  of lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y': newpipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAcc = -8   # velocity of flapping 
    playerFlapped = False   # it is true only when the bird is flapping


    while True :
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_SPACE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)  # this function will return true if the player is crashed
        if crashTest:
            return
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pillar'][0].get_width()/2
            if pipeMidPos<= playerMidPos< pipeMidPos+4:
                score+=1
                print (f"Your score is {score} ") 
                GAME_SOUNDS['point'].play()

        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+= playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight= GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,GROUNDY-playery-playerHeight)

        #move pipe to left 
        for upperPipe, lowerPipe in zip (upperPipes,lowerPipes):
            upperPipe['x']+= pipeVelX
            lowerPipe['x']+= pipeVelX
        #add a nwe pipe when the first is about to cross the leftmost part of the screen 
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])    

        #if the pipe is out of the screen ,remove it
        if upperPipes[0]['x']< -GAME_SPRITES['pillar'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Lets blit our sprits 
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe, lowerPipe in zip (upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pillar'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pillar'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int (x) for x in list (str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+= GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)        


        



 


def isCollide(playerx ,playery ,upperPipes,lowerPipes):
    if playery>GROUNDY -25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pillar'][0].get_height()
        if(playery< pipeHeight + pipe['y'] and abs(playerx - pipe['x'])<GAME_SPRITES['pillar'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pillar'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False





def getRandomPipe():
    # generate position of two pipes for blitting on the screen

    pipeHeight = GAME_SPRITES['pillar'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight-y2 + offset
    pipe = [
        
         {'x':pipeX, 'y':-y1},
         {'x':pipeX, 'y':y2},
        
    ]
    return pipe


if __name__=="__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird By Bhavesh")
    GAME_SPRITES['numbers']=(
        pygame.image.load('Gallery/sprites/0-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/1-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/2-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8-Number-PNG.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/9-Number-PNG.png').convert_alpha(),
    )

GAME_SPRITES['message'] = pygame.image.load('Gallery/sprites/message.png').convert_alpha()
GAME_SPRITES['base'] = pygame.image.load('Gallery/sprites/base.png').convert_alpha()
GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
GAME_SPRITES['pillar'] =(

    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
)

GAME_SOUNDS['die']= pygame.mixer.Sound('Gallery/audio/die.mp3')
GAME_SOUNDS['hit']= pygame.mixer.Sound('Gallery/audio/hit.mp3')
GAME_SOUNDS['point']= pygame.mixer.Sound('Gallery/audio/point.mp3')
GAME_SOUNDS['swoosh']= pygame.mixer.Sound('Gallery/audio/swoosh.mp3')
GAME_SOUNDS['wing']= pygame.mixer.Sound('Gallery/audio/wing.mp3')


while True:
    WelcomeScreen()
    mainGame()