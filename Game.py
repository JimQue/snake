import pygame
import classes


#variables
height = 600    #height of window
width = 500     #width of window
grid_height = 500
win = pygame.display.set_mode((width, height))
gap = width // 20  #gap between each line
#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
#game score
score = 0
#background images
background = pygame.image.load('imgs/bg.jpg')
background = pygame.transform.scale(background, (width, height))
#restart icon
restart_img = pygame.image.load('imgs/restart.png')
r_h = restart_img.get_height()
r_w = restart_img.get_width()
restart_clicked_img = pygame.transform.scale(restart_img, (round(r_w * 0.5), round(r_h * 0.5)))
#initialization
mysnake = classes.snake(win, width//2, grid_height//2, red, blue, gap, width, grid_height, gap)
myFood = classes.food(win, green, gap)
#initialize background object
bg = classes.bg(win, background, 0, 0)
#initialzie restart object
function_bar_height = height - grid_height
restart = classes.button(win, restart_img, (width - r_w)//2, grid_height + (function_bar_height - r_h)//2)



#snake eating food
def eat():
    global myFood, mysnake
    if mysnake.head.x == myFood.x and mysnake.head.y == myFood.y:
        #growing
        tail = mysnake.body[-1]
        newCube = classes.cube(win, mysnake.bodyColor, tail.x - tail.dx*gap, tail.y - tail.dy*gap, tail.dx, tail.dy, tail.vel, width, grid_height, gap)
        mysnake.body.append(newCube)
        myFood = classes.food(win, green, gap)
        score += 1


#drawing grid
def drawGrid():
    x = 0
    y = 0
    while x <= width:
        pygame.draw.line(win, white, (x, 0), (x, grid_height))
        x += gap
    while y <= grid_height:
        pygame.draw.line(win, white, (0, y), (width, y))
        y += gap


#refresh everything displayed on window
def redraw():
    global mysnake
    bg.draw()
    restart.draw()
    drawGrid()
    myFood.draw()
    mysnake.move()
    eat()


#create new snake and restart game
def replay():
    global mysnake, score
    mysnake = classes.snake(win, width//2, grid_height//2, red, blue, gap, width, grid_height, gap)
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
            restart.x = (width - restart.img.get_width()) // 2
            restart.y = grid_height + (function_bar_height - restart.img.get_height()) // 2
        else:
            restart.img = restart_img
            restart.x = (width - restart.img.get_width()) // 2
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
        replay()
    pygame.display.update()