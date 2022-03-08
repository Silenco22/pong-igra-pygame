import pygame
import math
import random

class Ball:
    WHITE = (255,255,255)
    COLOR = WHITE
    #ball radius
    RADIUS = 7
    #velocity of how FAST will ball move once we start
    MAX_VEL = 5
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL
    
    #every time we reset the ball it will start moving in random angle/direction
    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        
        return angle

    def draw(self, win):
        #drawing rectangle (we need window, color(cordinate x and y), radius)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.RADIUS )
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL

        self.y_vel = y_vel
        self.x_vel *= -1