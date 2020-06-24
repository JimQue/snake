import pygame

#variables
height = 500    #height of window
width = 500     #width of window
window = pygame.display.set_mode((height, width))
#colors
black = (0,0,0)
white = (255, 255, 255)




#refresh everything displayed on window
def redraw():
    window.fill(white)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    redraw()
    pygame.display.update()