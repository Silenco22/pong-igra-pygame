import pygame
#creating paddles

class Paddle:
    WHITE = (255,255,255)
    #values for width and height or the paddle
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    COLOR = WHITE
    #velocity of how much will paddles move once we hit up or down key 
    VEL = 4

    #intialize x,y cordinates where to draw and witdt and height of rectangle how big to draw
    def __init__(self, x, y):
        self.x = self.orginial_x = x
        self.y = self.orginial_y = y
       
    
    def draw(self, win):
        #drawing rectangle (we need window, color(cprdinate x and y, width, height))
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT) )

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self):
        self.x = self.orginial_x
        self.y = self.orginial_y
