#Brownian Motion Simulation
import math
import numpy
import pygame
import random
import time
inc = 0.1
kb = 1.380649* 10 **-13
distance = lambda p1, p2: ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) **0.5
print("Start")
class ball:
    #initialize
    def  __init__(self, vx, vy, m, r, posX, posY):
        self.v = [vx , vy ]
        self.m = m
        self.r = r*1.1
        self.pos = [posX, posY]
        self.color = "red"
    #collide
    def addVel(self):
        self.v=[self.v[0]+ random.gauss(0,10)/20, self.v[1] + random.gauss(0,10)/20]
    def collide(self, ball2):
        dist = distance(ball2.pos, self.pos)
        dawg = ball2.r + self.r - dist 
        if(dawg > 0):
            rt2 = 2 **0.5
            addy =  dawg/rt2
            max(ball2, self, key = lambda a: a.pos[0]).pos[0] += addy 
            max(ball2, self, key = lambda a: a.pos[1]).pos[1] += addy
        dist = distance(ball2.pos, self.pos)  
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
        if(self.pos[0] - self.r < 0):
            self.pos[0] = self.r
        else:
            self.pos[0] = 1280 - self.r
    def ceilingBounce(self):
        self.v[1] = -1 * self.v[1]
        if(self.pos[1] - self.r <= 0):
            self.pos[1] = self.r
        else:
            self.pos[1] = 720 - self.r
    def kineticEnergy(self):
        return 0.5*self.m*(self.v[0]**2 + self.v[1]**2)
class ensemble:
    balls = []
    original = []
    def __init__(self):
        self.balls = []
    def findTemp(self):
        return kb * 1.5 * sum([i.kineticEnergy() for i in self.balls])/len(self.balls)
    def addBalls(self, count):
        for i in range(count):
            antonio = ball(random.randint(-10,10),random.randint(-10,10),10,10, random.randint(200,1200), random.randint(200,400))
            self.balls.append(antonio)
        for i in range(count):
            self.original.append(self.balls[i].pos)
    def MSD(self):
        return sum([distance(self.balls[i].pos, self.original[i]) **2 for i in range(len(self.balls))])/len(self.balls)
    def collisions(self):
        alrDone = set()
        for i in self.balls:
            for j in self.balls:
                if i is not j and (j, i) not in alrDone:
                    if distance(i.pos, j.pos) <= i.r + j.r:
                        i.collide(j)
                alrDone.add((i,j))
        for i in self.balls:
            if(abs((i.pos[0] +i.r)- 640) >= 640 or i.pos[0] <=i.r):
                i.wallBounce()
            if(abs((i.pos[1] +i.r)- 360) >= 360 or i.pos[1] <=i.r):
                i.ceilingBounce()
    def randomCollision(self):
        for i in self.balls:
            i.addVel()
            if(abs((i.pos[0] +i.r)- 640) >= 640 or i.pos[0] <=i.r):
                i.wallBounce()
            if(abs((i.pos[1] +i.r)- 360) >= 360 or i.pos[1] <=i.r):
                i.ceilingBounce()
    def drawDawg(self):
        rtn =[]
        for i in self.balls:
            rtn.append((i.pos[0], i.pos[1], i.r))
        return rtn
    def advance(self):
        for i in self.balls:
            i.pos = [i.pos[0] + i.v[0], i.pos[1] + i.v[1]]



cnt = 0
MeanMSD= 0
start_time1 = time.time()
for i in range(5):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    joe = []
    Group = ensemble()
    Group.addBalls(200)
    points = []
    cnt = 0
    
    while cnt < 100 and running:
        myFont = pygame.font.SysFont("Times New Roman", 18)
        Disp = myFont.render(str(Group.findTemp()), True, 1)
        cnt += 1
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        #handle collisons
        
        Group.collisions()
        Group.advance()
        atro = 0
        
        for i in Group.drawDawg():
            #print(i)
            atro += 1
            if(atro == 1):
                pygame.draw.circle(screen, "red", i[:2], i[2])
            else:
                pygame.draw.circle(screen, "blue", i[:2], i[2])
        if(len(points) > 2):
            pygame.draw.lines(screen,"green", False,points, 0)
        if(cnt > 100):
            points.append(Group.balls[0].pos)
        screen.blit(Disp,(520,30))
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
runtime1 = time.time() - start_time1
print("second")
start_time2 = time.time()
for i in range(5):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    joe = []
    Group = ensemble()
    Group.addBalls(200)
    points = []
    cnt = 0
    
    while cnt < 100 and running:
        #myFont = pygame.font.SysFont("Times New Roman", 18)
        #Disp = myFont.render(str(Group.findTemp()), True, 1)
        cnt += 1
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")
        #handle collisons
        
        Group.randomCollision()
        Group.advance()
        atro = 0
        
        for i in Group.drawDawg():
            #print(i)
            atro += 1
            if(atro == 1):
                pygame.draw.circle(screen, "red", i[:2], i[2])
            else:
                pygame.draw.circle(screen, "blue", i[:2], i[2])
        if(len(points) > 2):
            pygame.draw.lines(screen,"green", False,points, 0)
        if(cnt > 100):
            points.append(Group.balls[0].pos)
        screen.blit(Disp,(520,30))
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    MeanMSD += Group.MSD()
runtime2 = time.time() - start_time2
import matplotlib.pyplot as plt


programs = ['Classical', 'Statistical']
runtimes = [runtime1, runtime2]


plt.bar(programs, runtimes, color=['blue', 'green'])
plt.xlabel('Programs')
plt.ylabel('Runtime (seconds)')
plt.title('Comparison of Runtimes')
plt.show()

