import random
import pygame



# movable cubes that will compose the body of the snake
class cube():
    def __init__(self, surface, color, x, y, dx, dy, vel, x_bound, y_bound, size):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.vel = vel
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.size = size

    def move(self):
        x = self.x + self.dx * self.vel
        y = self.y + self.dy * self.vel
        if x >= self.x_bound:
            x = 0
        if x < 0:
            x = self.x_bound - self.vel
        if y >= self.y_bound:
            y = 0
        if y < 0:
            y = self.y_bound - self.vel
        self.x = x
        self.y = y
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.size, self.size))


class snake():
    def __init__(self, surface, x, y, headColor, bodyColor, vel, x_bound, y_bound, size):
        self.surface = surface
        self.headColor = headColor
        self.bodyColor = bodyColor
        self.x_bound = x_bound
        self.y_bound = y_bound
        self.size = size
        self.head = cube(self.surface, self.headColor, x, y, 0, 0, vel, self.x_bound, self.y_bound, self.size)
        self.body = [self.head]
        self.turningPoints = {}  # points where the head turns and the direction

    def move(self):
        points = self.turningPoints.keys()
        for c in self.body:
            # check if cube in turning points, and modify direction accordingly
            if (c.x, c.y) in points:
                turn = self.turningPoints[(c.x, c.y)]
                c.dx = turn[0]
                c.dy = turn[1]
                # if cube is the tail of the snake, delete the point from turingpoints list after the tail gets through
                if c == self.body[-1]:
                    self.turningPoints.pop((c.x, c.y))
            c.move()

    # check if die
    def die(self):
        realBody = self.body[1:]
        headPos = (self.head.x, self.head.y)
        for c in realBody:
            if headPos == (c.x, c.y):
                return True
        return False

#food class
class food():
    def __init__(self, surface, color, size):
        x = random.randint(0, 19)
        y = random.randint(0, 19)
        self.surface = surface
        self.color = color
        self.size = size
        self.x = x * size
        self.y = y * size

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.size, self.size))


# background image class
class bg():
    def __init__(self,surface, img, x, y):
        self.surface = surface
        self.snake = snake
        self.x = x
        self.y = y
        self.img = img

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))

#button class
class button():
    def __init__(self, surface, img, x, y):
        self.surface = surface
        self.snake = snake
        self.x = x
        self.y = y
        self.img = img
        self.clicked = False

    def draw(self):
        self.surface.blit(self.img, (self.x, self.y))





