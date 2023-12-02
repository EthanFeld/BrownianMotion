#Brownian Motion Simulation
import math
import numpy
import pygame
import random
inc = 0.1
kb = 1.380649* 10 **-13
distance = lambda p1, p2: ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) **0.5

class ball:
    #initialize
    def  __init__(self, vx, vy, m, r, posX, posY):
        self.v = [vx, vy]
        self.m = m
        self.r = r
        self.pos = [posX, posY]
    #collide
    def collide(self, ball2):
        #variables
        vx1, vy1 = self.v
        x1,y1 = self.pos
        vx2, vy2 = ball2.v
        x2,y2 = ball2.pos
        #find relative 
        dx = x1 - x2
        dy = y1 - y2
        dvx = vx1 - vx2
        dvy = vy1 - vy2
        dist = max(distance(ball2.pos, self.pos), 0.00001)
        cosTheta = (dy)/dist
        sinTheta = (dx)/dist
        vx1n = vx1 + sinTheta*( -vx1*sinTheta + vx2*sinTheta - vy1*cosTheta + vy2*cosTheta)
        vy1n = vy1 + cosTheta*(-vx1*sinTheta + vx2*sinTheta - vy1*cosTheta + vy2*cosTheta)
        vx2n = vx2 + vx1 - vx1n
        vy2n = vy2 + vy1 - vy1n
        ball2.v = [vx2n, vy2n]
        self.v = [vx1n, vy1n]
    def wallBounce(self):
        self.v[0] = -1 * self.v[0] 
    def ceilingBounce(self):
        self.v[1] = -1 * self.v[1]
    def kineticEnergy(self):
        return 0.5*m*v**2
class ensemble:
    balls = []
    def __init__(self):
        self.balls = []
    def findTemp(self):
        return kb * 1.5 * [i.kineticEnergy(i) for i in self.balls]
    def addBalls(self, count):
        for i in range(count):
            antonio = ball(random.randint(-10,10),random.randint(-10,10),10,10, random.randint(200,1200), random.randint(200,400))
            self.balls.append(antonio)
    def collisions(self):
        alrDone = set()
        for i in self.balls:
            
            for j in self.balls:
                if i is not j and (j, i) not in alrDone:
                    if distance(i.pos, j.pos) <= i.r + j.r:
                        i.collide(j)
                alrDone.add((i,j))
        for i in self.balls:
            if(abs((i.pos[0] +i.r)- 640) >= 640):
                i.wallBounce()
            if(abs((i.pos[1] +i.r)- 360) >= 360):
                i.ceilingBounce()
    def drawDawg(self):
        rtn =[]
        for i in self.balls:
            rtn.append((i.pos[0], i.pos[1], i.r))
        return rtn
    def advance(self):
        for i in self.balls:
            i.pos = [i.pos[0] + i.v[0], i.pos[1] + i.v[1]]

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
joe = []
Group = ensemble()
Group.addBalls(200)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    #handle collisons
    Group.collisions()
    Group.advance()
    for i in Group.drawDawg():
        #print(i)
        pygame.draw.circle(screen, "red", i[:2], i[2])
    
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

