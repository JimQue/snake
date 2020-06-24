import pygame
import random

#variables
height = 500    #height of window
width = 500     #width of window
win = pygame.display.set_mode((height, width))
gap = height // 20  #gap between each line
#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


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
        pygame.draw.rect(win, self.color, (self.x, self.y, gap, gap))
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed



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
#initialize snake
mysnake = snake(gap,250, red, blue)



#initialize food
def generateFood():
    x = random.randint(0, 19)
    y = random.randint(0, 19)
    return cube(green, x*gap, y*gap, 0, 0 , 0)

myFood = generateFood()


#snake eating food
def eat():
    global myFood
    if mysnake.head.x == myFood.x and mysnake.head.y == myFood.y:
        #growing
        tail = mysnake.body[-1]
        newCube = cube(mysnake.bodyColor, tail.x - tail.dx*gap, tail.y - tail.dy*gap, tail.dx, tail.dy, tail.speed)
        mysnake.body.append(newCube)
        myFood = generateFood()




#drawing grid
def drawGrid():
    x = 0
    y = 0
    while x <= width:
        pygame.draw.line(win, black, (x, 0), (x, height))
        x += gap
    while y <= height:
        pygame.draw.line(win, black, (0, y), (width, y))
        y += gap


#refresh everything displayed on window
def redraw():
    win.fill(white)     #make the background white
    drawGrid()
    mysnake.move()
    myFood.move()
    eat()
   

#game loop
while True:
    clock = pygame.time.Clock()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mysnake.head.dy = -1
                mysnake.head.dx = 0
                mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (0, -1)
            if event.key == pygame.K_DOWN:
                mysnake.head.dy = 1
                mysnake.head.dx = 0
                mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (0, 1)
            if event.key == pygame.K_LEFT:
                mysnake.head.dy = 0
                mysnake.head.dx = -1
                mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (-1, 0)
            if event.key == pygame.K_RIGHT:
                mysnake.head.dy = 0
                mysnake.head.dx = 1
                mysnake.turningPoints[(mysnake.head.x, mysnake.head.y)] = (1, 0)
    
    redraw()
    pygame.display.update()