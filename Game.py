import pygame
import classes
import pickle

pygame.init()
pygame.display.set_caption('snake')
#variables
height = 1000   #height of window
grid_width = 800
grid_height = 800
win = pygame.display.set_mode((grid_width, height))
gap = grid_width // 20  #gap between each line
#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
pink = (255,192,203)
brown = (165,42,42)
#game score
score = 0
record = []
#background images
background = pygame.image.load('imgs/bg.jpg')
background = pygame.transform.scale(background, (grid_width, height))
#restart icon
restart_img = pygame.transform.scale2x(pygame.image.load('imgs/restart.png'))
r_h = restart_img.get_height()
r_w = restart_img.get_width()
#smaller image for hover effect
restart_clicked_img = pygame.transform.scale(restart_img, (round(r_w * 0.5), round(r_h * 0.5)))
#initialization
mysnake = classes.snake(win, grid_width // 2, grid_height // 2, pink, purple, gap, grid_width, grid_height, gap)
myFood = classes.food(win, brown, gap)
#initialize background object
bg = classes.bg(win, background, 0, 0)
#initialzie restart object
function_bar_height = height - grid_height
restart = classes.button(win, restart_img, (grid_width - r_w) // 2, grid_height + (function_bar_height - r_h) // 2)
#reading score records from pickled file
try:
    record = pickle.load(open('record', 'rb'))
except FileNotFoundError:
    pickle.dump(record, open('record', 'wb'))

    
#update record
def update():
    global record, score
    record = pickle.load(open('record', 'rb'))
    record.append(score)
    print(record)
    pickle.dump(record, open('record', 'wb'))
    score = 0

#get highest score
def get_heighest():
    global record
    record = pickle.load(open('record', 'rb'))
    return str(max(record))


#display text
def message_display(surface, text, x):
    myfont = pygame.font.Font('freesansbold.ttf',60)
    sur = myfont.render(text, True, purple)
    y = grid_height + function_bar_height//2
    text_rect = sur.get_rect()
    text_rect.center = (x, y)
    surface.blit(sur, text_rect)


#snake eating food
def eat():
    global myFood, mysnake, score
    if mysnake.head.x == myFood.x and mysnake.head.y == myFood.y:
        #growing
        tail = mysnake.body[-1]
        newCube = classes.cube(win, mysnake.bodyColor, tail.x - tail.dx * gap, tail.y - tail.dy * gap, tail.dx, tail.dy, tail.vel, grid_width, grid_height, gap)
        mysnake.body.append(newCube)
        myFood = classes.food(win, brown, gap)
        score += 1


#drawing grid
def drawGrid():
    x = 0
    y = 0
    while x <= grid_width:
        pygame.draw.line(win, white, (x, 0), (x, grid_height))
        x += gap
    while y <= grid_height:
        pygame.draw.line(win, white, (0, y), (grid_width, y))
        y += gap


#refresh everything displayed on window
def redraw():
    global mysnake
    bg.draw()
    restart.draw()
    myFood.draw()
    mysnake.move()
    drawGrid()
    eat()
    #show current score
    message_display(win, "score:" + str(score), (grid_width - r_w) // 4)
    #show highest record
    message_display(win, 'record:' + get_heighest(), grid_width - (grid_width - r_w) // 4)


#create new snake and restart game
def replay():
    global mysnake, score
    mysnake = classes.snake(win, grid_width // 2, grid_height // 2, pink, purple, gap, grid_width, grid_height, gap)
    score = 0

#game loop
while True:
    clock = pygame.time.Clock()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        #mouse click detection
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pos[0] >= restart.x and pos[0] <= restart.x + r_w and pos[1] >= restart.y and pos[1] <= restart.y + r_h:
                replay()
        #hover effect
        if pos[0] >= restart.x and pos[0] <= restart.x + r_w and pos[1] >= restart.y and pos[1] <= restart.y + r_h:
            restart.img = restart_clicked_img
            restart.x = (grid_width - restart.img.get_width()) // 2
            restart.y = grid_height + (function_bar_height - restart.img.get_height()) // 2
        else:
            restart.img = restart_img
            restart.x = (grid_width - restart.img.get_width()) // 2
            restart.y = grid_height + (function_bar_height - restart.img.get_height()) // 2

    #directions control
    keys = pygame.key.get_pressed()
    turnPos = mysnake.turningPoints.keys()
    if (mysnake.head.x, mysnake.head.y) not in turnPos:         #can't turn to two different directions at the same time
        if keys[pygame.K_UP] and (mysnake.head.dy != 1 or len(mysnake.body) == 1):
            mysnake.head.dy = -1
            mysnake.head.dx = 0
            mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (0, -1)
        elif keys[pygame.K_DOWN] and (mysnake.head.dy != -1  or len(mysnake.body) == 1):
            mysnake.head.dy = 1
            mysnake.head.dx = 0
            mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (0, 1)
        elif keys[pygame.K_LEFT] and (mysnake.head.dx != 1  or len(mysnake.body) == 1):
            mysnake.head.dy = 0
            mysnake.head.dx = -1
            mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (-1, 0)
        elif keys[pygame.K_RIGHT] and (mysnake.head.dx != -1  or len(mysnake.body) == 1):
            mysnake.head.dy = 0
            mysnake.head.dx = 1
            mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (1, 0)

    
    redraw()
    #if die, restart
    if mysnake.die():
        update()
        replay()
    pygame.display.update()