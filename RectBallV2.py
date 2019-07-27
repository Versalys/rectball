'''
 ______     ______     ______     ______             ______     ______     __         __
/\  == \   /\  ___\   /\  ___\   /\__  _\   ____    /\  == \   /\  __ \   /\ \       /\ \
\ \  __<   \ \  __\   \ \ \____  \/_/\ \/  |____|   \ \  __<   \ \  __ \  \ \ \____  \ \ \____
 \ \_\ \_\  \ \_____\  \ \_____\    \ \_\            \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\
  \/_/ /_/   \/_____/   \/_____/     \/_/             \/_____/   \/_/\/_/   \/_____/   \/_____/

 Created by Aidan Erickson, Based on the popular IOS game: Head Soccer.
 Created for the AP Computer Science create task project 2019.
'''

import pygame as pg

pg.init()

#Display parameters
disX = 1250
disY = 675
myDisplay = pg.display.set_mode((disX, disY))

pg.display.set_caption("Rectangle Ball")

plOneScore = 0
plTwoScore = 0

#Movement variables
plOneX = 50
plOneY = 50
width = 60
height = 160
vel = 20
plTwoX = disX - plOneX - width
plTwoY = 50

verVel = 0
verVel2 = 0
accel = 3.5

kicking1 = False
kicking2 = False

bWidth = 30
bHeight = 30
ballX = disX/2 - bWidth/2
ballY = bHeight + 50
ballVel = 0
bHorVel = 0

gWidth = 40
gHeight = 150

bluePlayer = pg.Rect(plOneX, plOneY, width, height)
redPlayer = pg.Rect(plTwoX, plTwoY, width, height)
ballRect = pg.Rect(ballX, ballY, bWidth, bHeight)
screenRect = pg.Rect(0, 0, disX, disY)
goal1 = pg.Rect(0, disY - gHeight, gWidth, gHeight)
goal2 = pg.Rect(disX - gWidth, disY - gHeight, gWidth, gHeight)

#Jumping variables
jumping = True
jumping2 = True
bFalling = True

devCheat = False
running = True

#MAIN-LOOP
while running:
    pg.time.delay(25)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

#Falling physics
    if plOneY < disY - height:
        plOneY += verVel
        verVel += accel
    if plOneY + height > disY and jumping:
        plOneY = disY - height
        jumping = False
    if jumping:
        plOneY += verVel

    if plTwoY < disY - height:
        plTwoY += verVel2
        verVel2 += accel
    if plTwoY + height > disY and jumping2:
        plTwoY = disY - height
        jumping2 = False
    if jumping2:
        plTwoY += verVel2

    ballY += ballVel
    ballX += bHorVel
    if ballVel < 1.5 and ballVel > -1.5 and ballY > disY - bHeight - 5:
        ballVel = 0
        bHorVel = 0
        ballY = disY - bHeight
        bFalling = False
    if ballY < disY - bHeight:
        ballVel += accel
        bFalling = True
    elif bFalling:
        ballVel *= -3/4
        bHorVel *= 3/4
        bFalling = False

    #Ball clipping
    if ballY > disY + 10:
        ballY = disY - bHeight - 10
        falling = True

#Key event if structure
    keys = pg.key.get_pressed()
    if keys[pg.K_a] and plOneX > vel:
        plOneX -= vel
    if keys[pg.K_d] and plOneX < disX - width - vel:
        plOneX += vel
    if keys[pg.K_w] and not jumping and not devCheat:
        jumping = True
        verVel = -40

    if keys[pg.K_LEFT] and plTwoX > vel:
        plTwoX -= vel
    if keys[pg.K_RIGHT] and plTwoX < disX - width - vel:
        plTwoX += vel
    if keys[pg.K_UP] and not jumping2 and not devCheat:
        jumping2 = True
        verVel2 = -40

        #Ball reset
    if keys[pg.K_EQUALS]:
        bHorVel = 0
        ballVel = 0
        ballY = bHeight + 50
        ballX = disX / 2 - bWidth / 2

        #DEV TESTING HOT-KEYS
    if keys[pg.K_LEFTBRACKET]:
        if devCheat:
            devCheat = False
            print("dev-cheat enabled")
        else:
            devCheat = True
    if devCheat:
        if keys[pg.K_BACKSLASH]:
            print("X: " + str(plOneX) + " Y: " + str(plOneY))
        if keys[pg.K_COMMA]:
            bHorVel -= 20
            ballVel = -10
            bFalling = True
        if keys[pg.K_PERIOD]:
            bHorVel += 20
            ballVel = -10
            bFalling = True

    #Colision and more physics
    if ballRect.colliderect(bluePlayer) or ballRect.colliderect(redPlayer):
        if bFalling:
            if ballRect.colliderect(bluePlayer) and kicking1 is False:
                kicking1 = True
                #pl1Kick = kickCount
                bHorVel = 40
                ballVel -= 20
                #print("falling collision")
            if ballRect.colliderect(redPlayer) and kicking2 is False:
                kicking2 = True
                #pl2Kick = kickCount
                bHorVel = -40
                ballVel -= 20
                #print("falling collision")
        else:
            bFalling = True
            if ballRect.colliderect(bluePlayer) and kicking1 is False:
                if ballRect.midleft <= bluePlayer.midright:
                    bHorVel = 5
                    ballVel = -5
                    #print("Bleft")
                elif ballRect.midright >= bluePlayer.midleft:
                    bHorVel = -20
                    ballVel = -30
                    #print("Bright")
                elif ballRect.midtop <= bluePlayer.midbottom:
                    bHorVel = 20 * random.randrange(-1, 1)
                    ballVel = -5
                    #print("Bbottom")
                kicking1 = True
            elif kicking2 is False:
                if ballRect.midright >= redPlayer.midleft:
                    bHorVel = -20
                    ballVel = -30
                    #print("Rright")
                elif ballRect.midleft <= redPlayer.midright:
                    bHorVel = 20
                    ballVel = -30
                    #print("Rleft")
                elif ballRect.midtop <= redPlayer.midbottom:
                    bHorVel = 20 * random.randrange(-1, 1)
                    ballVel = -5
                    #print("Rbottom")
                kicking2 = True

    if screenRect.midleft >= ballRect.midleft:
        bHorVel = bHorVel * -4/5
        #print("Screen left")
        ballX = 1
    if screenRect.midright <= ballRect.midright:
        bHorVel = bHorVel * -4/5
        #print("Screen right")
        ballX = disX - bWidth - 1

    if ballRect.colliderect(bluePlayer):
        kicking1 = True
    else:
         kicking1 = False
    if ballRect.colliderect(redPlayer):
        kicking2 = True
    else:
        kicking2 = False

    if ballRect.colliderect(goal1) or ballRect.colliderect(goal2):
        if ballRect.colliderect(goal1):
            plTwoScore += 1
        elif ballRect.colliderect(goal2):
            plOneScore += 1
        bHorVel = 0
        ballVel = 0
        ballY = bHeight + 50
        ballX = disX / 2 - bWidth / 2

    myDisplay.fill((0, 0, 0))

    bluePlayer = pg.Rect(plOneX, plOneY, width, height)
    redPlayer = pg.Rect(plTwoX, plTwoY, width, height)
    ballRect = pg.Rect(ballX, ballY, bWidth, bHeight)

    pg.draw.rect(myDisplay, (255, 0, 0), redPlayer)  #red player
    pg.draw.rect(myDisplay, (0, 0, 255), bluePlayer)  #blue player
    pg.draw.rect(myDisplay, (255, 255, 255), ballRect)  #Ball
    pg.draw.rect(myDisplay, (0, 255, 0), goal1)
    pg.draw.rect(myDisplay, (0, 255, 0), goal2)

    myFont = pg.font.SysFont('Arial', 80)
    renderedFont = myFont.render(str(plOneScore), 1, (100, 100, 255))
    renderedFont2 = myFont.render(str(plTwoScore), 1, (255, 100, 100))
    myDisplay.blit(renderedFont, (100, 100))
    myDisplay.blit(renderedFont2, (disX - 100 - 80, 100))

    pg.display.update()

'''
 _______   __                                                __       __                      __       
/       \ /  |                                              /  |  _  /  |                    /  |      
$$$$$$$  |$$ |  ______    ______    _______   ______        $$ | / \ $$ |  ______    ______  $$ |   __ 
$$ |__$$ |$$ | /      \  /      \  /       | /      \       $$ |/$  \$$ | /      \  /      \ $$ |  /  |
$$    $$/ $$ |/$$$$$$  | $$$$$$  |/$$$$$$$/ /$$$$$$  |      $$ /$$$  $$ |/$$$$$$  |/$$$$$$  |$$ |_/$$/ 
$$$$$$$/  $$ |$$    $$ | /    $$ |$$      \ $$    $$ |      $$ $$/$$ $$ |$$ |  $$ |$$ |  $$/ $$   $$<  
$$ |      $$ |$$$$$$$$/ /$$$$$$$ | $$$$$$  |$$$$$$$$/       $$$$/  $$$$ |$$ \__$$ |$$ |      $$$$$$  \ 
$$ |      $$ |$$       |$$    $$ |/     $$/ $$       |      $$$/    $$$ |$$    $$/ $$ |      $$ | $$  |
$$/       $$/  $$$$$$$/  $$$$$$$/ $$$$$$$/   $$$$$$$/       $$/      $$/  $$$$$$/  $$/       $$/   $$/ 
'''
