import pygame
import random

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
#background images
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (width, height))
background2 = pygame.transform.flip(background, True, False)




#movable cubes that will compose the body of the snake
class cube():
    def __init__(self, color, x, y, dx, dy, speed):
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
    

    def move(self):
        x =  self.x + self.dx * self.speed
        y =  self.y + self.dy * self.speed
        if x >= width:
            x = 0
        if x < 0:
            x = width - gap
        if y >= grid_height:
            y = 0
        if y < 0:
            y = grid_height - gap
        self.x = x
        self.y = y
        pygame.draw.rect(win, self.color, (self.x, self.y, gap, gap))



class snake():
    def __init__(self, x, y, headColor, bodyColor):
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.head = cube(self.headColor, x, y, 1, 0, gap)
        self.body = [self.head]
        self.turningPoints = {}     #points where the head turns and the direction
    
    def move(self):
        points = self.turningPoints.keys()
        for c in self.body:
            #check if cube in turning points, and modify direction accordingly
            if (c.x, c.y) in points:
                turn = self.turningPoints[(c.x, c.y)]
                c.dx = turn[0]
                c.dy = turn[1]
                #if cube is the tail of the snake, delete the point from turingpoints list after the tail gets through
                if c == self.body[-1]:
                    self.turningPoints.pop((c.x,c.y))
            c.move()

    #check if die
    def die(self):
        realBody = self.body[1:]
        headPos = (self.head.x, self.head.y)
        for c in realBody:
            if headPos == (c.x, c.y):
                return True
        return False


#background image class
class bg():
    def __init__(self, img, x, y):
        self.snake = snake
        self.x = x
        self.y = y
        self.img = img
    
    def draw(self):
        win.blit(background, (self.x, self.y))




#initialize food
def generateFood():
    x = random.randint(0, 19)
    y = random.randint(0, 19)
    return cube(green, x*gap, y*gap, 0, 0 , 0)

#initialize
mysnake = snake(gap,250, red, blue)
myFood = generateFood()
#initialize set of images
bg = bg(background, 0, 0)

# #draw background images
# def draw_bg():
#     if bg1.x <= -width:
#         bg1.x = width
#     if bg2.x <= -width:
#         bg2.x = width
#     bg1.move()
#     bg2.move()


#snake eating food
def eat():
    global myFood, mysnake
    if mysnake.head.x == myFood.x and mysnake.head.y == myFood.y:
        #growing
        tail = mysnake.body[-1]
        newCube = cube(mysnake.bodyColor, tail.x - tail.dx*gap, tail.y - tail.dy*gap, tail.dx, tail.dy, tail.speed)
        mysnake.body.append(newCube)
        myFood = generateFood()
        for c in mysnake.body:
            print((c.x, c.y))





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
    drawGrid()
    myFood.move()
    mysnake.move()
    eat()

   

#game loop
while True:
    clock = pygame.time.Clock()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        turnPos = mysnake.turningPoints.keys()
        if (mysnake.head.x, mysnake.head.y) not in turnPos:         #can't turn to two directions at the same time
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
        for c in mysnake.body:
            mysnake = snake(gap,250, red, blue)
    pygame.display.update()