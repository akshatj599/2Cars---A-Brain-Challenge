import pygame
import random
import math
from pygame import mixer

pygame.init()

# Creating Main Screen
screen = pygame.display.set_mode((850, 945))
pygame.display.set_caption("2 Cars")

# Images
def loadImage(imgname):
    return pygame.image.load(imgname).convert_alpha()
    #.convert_alpha() explained in the description of this function.

pygame.display.set_icon(pygame.image.load("MiniIcon.png"))
track = loadImage("Road.png")
carL = loadImage("CarLF.png")
carR = loadImage("CarRF.png")
circleL = loadImage("CircleL.png")
circleR = loadImage("CircleR.png")
blockL = loadImage("blockL.png")
blockR = loadImage("blockR.png")
startBack = loadImage("Start.png")
instructions = loadImage("Instructions.png")
lostBack = loadImage("Lose.png")
hit = loadImage("Hit.png")
miss = loadImage("Miss.png")
mini_icon = loadImage("MiniIcon.png")
fire = loadImage("fire.png")

# Music
pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.music.load("2Cars Background Track MP3.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.5);


def placeCarL(x, y):
    screen.blit(carL, (x, y))


def placeCarR(x, y):
    screen.blit(carR, (x, y))


def changeLaneL():
    global lState
    if (lState == "static"):
        lState = "changing"


def changeLaneR():
    global rState
    if (rState == "static"):
        rState = "changing"


def createObject(side):
    global LObjects, LObjects_y, LObjects_x, RObjects, RObjects_x, RObjects_y
    global LObjects_type, RObjects_type
    randLane = random.randint(1, 2)  # 1-L 2-R
    randObj = random.randint(3, 4)  # 3-circle #4-block
    if (side == "left"):  # For left side objects
        if (randLane == 1):  # |*| | | |
            if (randObj == 3):  # New circle
                LObjects.append(pygame.image.load("CircleL.png"))
                LObjects_type.append("c")
            else:  # New block
                LObjects.append(pygame.image.load("BlockL.png"))
                LObjects_type.append("b")
            LObjects_x.append(80)
            LObjects_y.append(-50)
        else:  # | |*| | |
            if (randObj == 3):  # New circle
                LObjects.append(pygame.image.load("CircleL.png"))
                LObjects_type.append("c")
            else:  # New block
                LObjects.append(pygame.image.load("BlockL.png"))
                LObjects_type.append("b")
            LObjects_x.append(275)
            LObjects_y.append(-50)

    else:  # For right side objects
        if (randLane == 1):  # | | |*| |
            if (randObj == 3):  # New circle
                RObjects.append(pygame.image.load("CircleR.png"))
                RObjects_type.append("c")
            else:  # New block
                RObjects.append(pygame.image.load("BlockR.png"))
                RObjects_type.append("b")
            RObjects_x.append(505)
            RObjects_y.append(-180)
        else:  # | | | |*|
            if (randObj == 3):  # New circle
                RObjects.append(pygame.image.load("CircleR.png"))
                RObjects_type.append("c")
            else:  # New block
                RObjects.append(pygame.image.load("BlockR.png"))
                RObjects_type.append("b")
            RObjects_x.append(705)
            RObjects_y.append(-180)


def placeObject(side, x, y, i):
    if (side == "left"):
        screen.blit(LObjects[i], (x, y))
    else:
        screen.blit(RObjects[i], (x, y))


def isCollision(objectX, objectY, carX, carY, i, side):
    global LObjects, LObjects_y, LObjects_x, RObjects, RObjects_x, RObjects_y, score
    global LObjects_typSe, RObjects_type, running
    distance = math.sqrt(math.pow(objectX - carX, 2) + math.pow(objectY - carY, 2))
    if (distance < 40):
        collect = mixer.Sound("Collect.wav")
        collect.set_volume(1.5)

        if (side == "left"):
            if (LObjects_type[i] == "c"):
                collect.play()
                LObjects.pop(i)
                LObjects_x.pop(i)
                LObjects_y.pop(i)
                LObjects_type.pop(i)
                score += 1
            else:
                gameOver("Hit", "Blue", "Block")

        else:
            if (RObjects_type[i] == "c"):
                collect.play()
                RObjects.pop(i)
                RObjects_x.pop(i)
                RObjects_y.pop(i)
                RObjects_type.pop(i)
                score += 1
            else:
                gameOver("Hit", "Orange", "Block")

#---------------------------------------------------------------------
def updateDifficulty(level):
    global difficulty, changeObj, distBtwObj
    difficulty = level
    if (level == "E"):
        changeObj = 2.0
        distBtwObj = 860
    elif (level == "M"):
        changeObj = 2.6
        distBtwObj = 720
    elif (level == "H"):
        changeObj = 3.0
        distBtwObj = 600
#---------------------------------------------------------------------

def update_Score():
    global score, difficulty, fire, changeObj

    # For Display
    font1 = pygame.font.Font('PenultimateLightItal_Regular.ttf', 35)
    font2 = pygame.font.Font('SEASRN_.ttf', 32)
    font5 = pygame.font.Font('PenultimateLightItal_Regular.ttf', 32)
    score_print = font1.render("Score: " + str(score), True, (255, 255, 255))
    if (difficulty == "E"):
        difficulty_print = font5.render("Easy", True, (14, 181, 56))
    elif (difficulty == "M"):
        difficulty_print = font5.render("Med", True, (222, 211, 13))
    elif (difficulty == "H"):
        difficulty_print = font5.render("Hard", True, (222, 68, 44))
    name_print = font2.render("2 CARS", True, (255, 255, 255))
    screen.blit(fire, (30, 16))
    screen.blit(score_print, (30, 50))
    screen.blit(difficulty_print, (65, 16))
    screen.blit(mini_icon, (232, 22))
    screen.blit(name_print, (272, 15))


def gameOver(how, color, object):
    global play, lost, lost_color, lost_how, lost_object
    lost_sound = mixer.Sound("lostsound.wav")
    lost_sound.set_volume(1.5)
    lost_sound.play()
    play = False
    lost = True
    lost_how = how
    lost_color = color
    lost_object = object


def reset():
    global lLane, rLane, lState, rState, score, just_started
    global xL, xR, farL, farR
    global LcurrY, LObjects, LObjects_x, LObjects_y, LObjects_type
    global RcurrY, RObjects, RObjects_x, RObjects_y, RObjects_type
    just_started = True
    score = 0
    lLane = "right"
    rLane = "left"
    lState = "static"
    rState = "static"
    xL = farL
    xR = farR
    LcurrY = 0
    RcurrY = 0
    LObjects = []
    LObjects_x = []
    LObjects_y = []
    LObjects_type = []
    RObjects = []
    RObjects_x = []
    RObjects_y = []
    RObjects_type = []

    placeCarL(60, 754)
    placeCarR(700, 750)
    createObject("left")
    createObject("right")


'''
lane coordinates:
Cars:
y =754 & 750
x values:
Left: l-> 60, r-> 260    far ends:#(50,         near ends:#(266, 
Right: l-> 490, r->700            #(700,                  #(484, 

Objects:
y-> 0 to 750 (vanish if hit or lose)
Left: l-> 80, r-> 275   
Right: l-> 505, r->705  
         
'''

# globals
running = True  # Main boolean
just_started = True  # For initial car movement

play = False  # For play mode
instruct = False  # For instruction screen
score = 0
lLane = "right"  # Denotes current sub-lane of each car
rLane = "left"
lState = "static"  # Condition of each car- whether it is static or changing lanes
rState = "static"

lost = False  # Becomes true if player loses, enables lost screen
lost_color = ""  # Indicates Color(Side) At Which Game Is Lost
lost_how = ""  # Indicates Reason Of Loss
lost_object = ""  # Indicates Object Of Loss

ObjLaneLl = 70  # Constant x coordinates of objects for all sub lanes
ObjLaneLr = 280
ObjLaneRl = 405
ObjLaneRr = 715

LcurrY = 0  # For creating new objects
RcurrY = 0

LObjects = []  # All left lane objects
LObjects_x = []
LObjects_y = []
LObjects_type = []

RObjects = []  # All right lane objects
RObjects_x = []
RObjects_y = []
RObjects_type = []
#---------------------------------------------------------------------
changeCar = 5
factor = 42
distBtwObj = 580 # distance between two consecutive objects on the same side
difficulty = "E"  # determines speed of movevment of cars
changeObj = 0  # speed of movement of objects
updateDifficulty("E")
#---------------------------------------------------------------------

farL = 50  # constants
farR = 700
xL = farL  # main variables - for every move in the program
xR = farR
nearL = farL + changeCar * factor  # derived formula # constants
nearR = farR - changeCar * factor

# Initial placement
placeCarL(60, 754)
placeCarR(700, 750)
createObject("left")
createObject("right")

while running:
    if (play == False):  # For Intermediate Screens
        # Lost Screen
        if (lost == True):
            screen.blit(track, (0, 0))
            placeCarL(50, 754)
            placeCarR(700, 750)
            screen.blit(lostBack, (0, 0))
            if (lost_how == "Hit"):
                screen.blit(hit, (30, 380))
            else:
                screen.blit(miss, (30, 380))
            font3 = pygame.font.Font('PenultimateLightItal_Regular.ttf', 55)
            message_print = font3.render("Pff... You " + lost_how + " A ", True, (255, 255, 255))
            screen.blit(message_print, (310, 400))
            message_print = font3.render(lost_color + " " + lost_object, True, (255, 255, 255))
            screen.blit(message_print, (310, 470))
            message_print = font3.render(f"Your Score: {score}", True, (255, 255, 255))
            screen.blit(message_print, (310, 540))
            font4 = pygame.font.Font('PenultimateLightItal_Regular.ttf', 45)
            if (difficulty == "E"):
                difficulty_print = font4.render("Easy", True, (14, 181, 56))
            elif (difficulty == "M"):
                difficulty_print = font4.render("Med", True, (222, 211, 13))
            elif (difficulty == "H"):
                difficulty_print = font4.render("Hard", True, (222, 68, 44))
            screen.blit(difficulty_print, (296, 814))



        else:
            # Start Screen
            if (instruct == False):
                screen.blit(track, (0, 0))
                placeCarL(50, 754)
                placeCarR(700, 750)
                screen.blit(startBack, (0, 0))
            # Instruction Screen
            else:
                font4 = pygame.font.Font('PenultimateLightItal_Regular.ttf', 45)
                if (difficulty == "E"):
                    difficulty_print = font4.render("Easy", True, (14, 181, 56))
                elif (difficulty == "M"):
                    difficulty_print = font4.render("Med", True, (222, 211, 13))
                elif (difficulty == "H"):
                    difficulty_print = font4.render("Hard", True, (222, 68, 44))
                screen.blit(track, (0, 0))
                placeCarL(50, 754)
                placeCarR(700, 750)
                screen.blit(instructions, (0, 0))
                screen.blit(difficulty_print, (320, 824))

        # Intermediate Screen Key Maps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE):
                    key_sound = mixer.Sound('KeyTap.wav')
                    key_sound.set_volume(1.3)
                    key_sound.play()
                if event.key == pygame.K_SPACE:

                    if (lost == True):
                        lost = False
                        play = True
                        reset()
                    if (instruct == True):
                        play = True  # Takes scope to Main Run
                        instruct = False
                        reset()
                    if (just_started == True or (instruct == False and lost == False)):
                        instruct = True

                if event.key == pygame.K_TAB:
                    if (instruct == True or lost == True):
                        if (difficulty == "E"):
                            updateDifficulty("M")
                        elif (difficulty == "M"):
                            updateDifficulty("H")
                        elif (difficulty == "H"):
                            updateDifficulty("E")

                if event.key == pygame.K_ESCAPE:
                    if (instruct == False and lost == False):
                        running = False
                    if (instruct == True):
                        instruct = False
                    if (lost == True):
                        lost = False
                        instruct = True


    else:  # Main Run - Play Mode
        screen.blit(track, (0, 0))

        if (just_started == True):
            xL += changeCar
            xR -= changeCar
            if (xL == nearL):
                just_started = False

        # Change lane & Exit Conditions (Key maps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    changeLaneL()
                if event.key == pygame.K_RSHIFT:
                    changeLaneR()

        # Movement & Creation Of Objects
        if (lState == "changing"):
            if (lLane == "right"):
                xL -= changeCar
                if (xL == farL):
                    lState = "static"
                    lLane = "left"
            if (lLane == "left"):
                xL += changeCar
                if (xL == nearL):
                    lState = "static"
                    lLane = "right"

        if (rState == "changing"):
            if (rLane == "left"):
                xR += changeCar
                if (xR == farR):
                    rState = "static"
                    rLane = "right"
            if (rLane == "right"):
                xR -= changeCar
                if (xR == nearR):
                    rState = "static"
                    rLane = "left"

        i = 0
        j = len(LObjects)
        while (i < j):
            LObjects_y[i] += changeObj
            if (LObjects_y[i] > 750 and LObjects_type[i] == "c"):
                gameOver("Missed", "Blue", "Circle")
                break
            placeObject("left", LObjects_x[i], LObjects_y[i], i)
            isCollision(LObjects_x[i], LObjects_y[i], xL, 754, i, "left")
            i += 1
            j = len(LObjects)

        i = 0
        j = len(RObjects)
        while (i < j):
            RObjects_y[i] += changeObj
            if (RObjects_y[i] > 750 and RObjects_type[i] == "c"):
                gameOver("Missed", "Orange", "Circle")
                break
            placeObject("right", RObjects_x[i], RObjects_y[i], i)
            isCollision(RObjects_x[i], RObjects_y[i], xR, 750, i, "right")
            i += 1
            j = len(RObjects)

        LcurrY += 4
        if (LcurrY > distBtwObj):
            createObject("left")
            LcurrY = 0

        RcurrY += 4
        if (RcurrY > distBtwObj):
            createObject("right")
            RcurrY = 0

        placeCarL(xL, 754)
        placeCarR(xR, 750)
        update_Score()

    pygame.display.update()

# png ,print game over
# x & y coordinates
# right objects appear late
# Change the logo

# For HeatStage update
# if score%10.0==0.0 and score/10.0!=0.0: #Increases at each increase of 50
#         changeObj+=0.1
#         heatStage+=1;
#         print(changeObj)
#         print(heatStage)
