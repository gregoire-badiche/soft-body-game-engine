#!/usr/bin/env python3

import pygame
import math
from random import randint
from time import perf_counter

G:float = .5
K:float = 3
INFINITY:int = 10000
cosmic_latte: tuple = (255,248,231)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

running = True
pressed=False
launched=False
angle=math.pi/6

pressed=False
launched=False
angle=math.pi/6
average:int =2              #average distance between the first and the last joint

class Score:
    def __init__(self) -> None:
        self.score=-1
        if self.score==-1:
            self.tic=round(perf_counter())
            self.score=0
            self.combo=1
        self.font_size=40
        self.coordinates=(1026, 180+(57-self.font_size)/2)
        self.font=pygame.font.Font("ressources/fonts/VeniteAdoremus-rgRBA.ttf", self.font_size)
        self.text=self.font.render("Score : {}".format(self.score), True, cosmic_latte)
        return
    def update(self, azer) -> None:
        
        
        joints_list = azer.get_joints()
        if (round(joints_list[0].getX())+average >= round(joints_list[len(joints_list)-1].getX()))and (round(joints_list[0].getX())-average <= round(joints_list[len(joints_list)-1].getX())):
            self.tac = round(perf_counter())
            if self.tac - self.tic <= 2:
                self.combo+=1
                self.score+=10*self.combo
                self.tic = self.tac 
            else: 
                self.score+=10
                self.tic = self.tac  
                self.combo = 1   
        self.text="Score : {}".format(self.score)
        if len(self.text)>9:
            self.font_size=int((50/len(self.text))*8)
            self.coordinates=(1026, 180+(57-self.font_size)/2)
            self.font=self.get_font(self.font_size)
        self.rendred=self.font.render(self.text, True, cosmic_latte)
       
        return
    def draw(self, azer) -> None:
        self.update(azer)
        screen.blit(self.rendred, self.coordinates)
        return
    def get_font(self, size):
        return pygame.font.Font("ressources/fonts/VeniteAdoremus-rgRBA.ttf", size)



class Joint:
    def __init__(self, x, y, distance:int, locked:bool = False, isedge:bool = False) -> None:
        self.x = x
        self.y = y
        self.speedx = 0
        self.speedy = 0
        self.prevx = x
        self.prevy = y
        self.isedge = isedge
        self.locked = locked
        self.distance = distance
        self.pspeedx = 0
        self.pspeedy = 0
        self.tx = 0
        self.ty = 0
        self.rx = 0
        self.ry = 0
        self.cx = 0
        self.cy = 0
        return
    
    def draw(self, x, y, *args):
        # pygame.draw.circle(screen, "black", (self.x, self.y), 10)
        pygame.draw.line(screen, "darkgoldenrod1", (self.x, self.y), (x, y), 11)
        pygame.draw.circle(screen, "black", (self.x, self.y), 5)
        # pygame.draw.circle(screen, "black", (x, y), 5)
        # pygame.draw.line(screen, "blue", (self.x, self.y), (self.x + self.speedx, self.y + self.speedy))
        return
    
    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        return
    
    def applygravity(self):
        if(self.locked): return
        self.speedy += G
        return

    def applytension(self):
        # Une fois que tous les vecteurs de tension calculés à partir des mêmes coordonnées, on peut enfin les appliquer sur le vecteur vitesse
        self.speedx += self.tx
        self.speedy += self.ty
        self.tx = 0
        self.ty = 0
        return
    
    def computetension(self, j):
        # Si le joint est bloqué dans l'espace, on ne fait rien
        if(self.locked): return
        # Différents coefficients :
        # m est à .5 si le joint j est libre, car ils s'attirent tous les deux avec une force opposée
        # et à 1 si le joint j est bloqué, car uniquement self est attiré (l'autre ne bouge pas)
        m = .5
        # mp est utilisé pour trouver le vecteur se situant entre la tension avec le joint d'après et celle avec le joint d'avant
        # si le joint est au bord, rien ne sert de faire la moyenne
        mp = .5
        if(j.locked == True):
            m = 1
        if(self.isedge):
            mp = 1
        x = self.x + self.speedx
        y = self.y + self.speedy
        xp = j.x + j.speedx
        yp = j.y + j.speedy
        # On prend la distance séparant les deux joints, afin d'appliquer Thalès sur x et y, pour les rapprocher
        dist = math.sqrt((x - xp) ** 2 + (y - yp) ** 2)
        if(dist != self.distance and dist != 0):
            # d * coeff (proportionnalité avec Thalès) * les différents coefficients
            self.tx += (x - xp) * (self.distance - dist) / dist * m * mp
            self.ty += (y - yp) * (self.distance - dist) / dist * m * mp
        return

    def checkfloor(self):
        if(self.y + self.speedy >= 600):
            self.y = 600
            if(self.speedy > 0):
                if(self.speedy > 1):
                    self.speedy = self.speedy * -0.5
                else:
                    self.speedy = 0
        return
    
    def applyreaction(self, s):
        f = s.projection((self.x + self.speedx, self.y + self.speedy))
        e = s.projection((self.x, self.y))
        # Adding a small padding to avoid glitching through
        # Change the value of d to make it bounce !!
        d = math.sqrt((f[0] - self.x -self.speedx) ** 2 + (f[1] - self.y - self.speedy) ** 2) * 100
        self.speedx = f[0] - self.x + (f[0] - self.x - self.speedx) / d
        self.speedy = f[1] - self.y + (f[1] - self.y - self.speedy) / d
        return
    
    def applyfriction(self):
        self.speedx *= .99
        self.speedy *= .99
        return
    
    def applyrigidity(self):
        self.speedx += self.rx
        self.speedy += self.ry
        self.rx = 0
        self.ry = 0
        return
    
    def computerigidity(self, j):
        # Si le joint est bloqué dans l'espace, on ne fait rien
        if(self.locked): return
        # Différents coefficients :
        # m est à .5 si le joint j est libre, car ils s'attirent tous les deux avec une force opposée
        # et à 1 si le joint j est bloqué, car uniquement self est attiré (l'autre ne bouge pas)
        m = .5
        # mp est utilisé pour trouver le vecteur se situant entre la tension avec le joint d'après et celle avec le joint d'avant
        # si le joint est au bord, rien ne sert de faire la moyenne
        mp = .5
        if(j.locked == True):
            m = 1
        if(self.isedge):
            mp = 1
        x = self.x + self.speedx
        y = self.y + self.speedy
        xp = j.x + j.speedx
        yp = j.y + j.speedy
        # On prend la distance séparant les deux joints, afin d'appliquer Thalès sur x et y, pour les écarter
        dist = math.sqrt((x - xp) ** 2 + (y - yp) ** 2)
        if(dist < self.distance * K):
            self.rx += (x - xp) * ((self.distance * K - dist) / (dist)) * m * mp
            self.ry += (y - yp) * ((self.distance * K - dist) / (dist)) * m * mp
        return
    def getX(self):
        return self.x

class Blob:
    def __init__(self, joints:list[Joint] = []) -> None:
        self.joints = joints
        return

    def __len__(self) -> int:
        return len(self.joints)

    def get_joints(self):
        return self.joints

    def addjoint(self, joint:Joint) -> int:
        self.joints.append(joint)
        return len(self.joints) - 1
    
    def fix(self) -> None:
        self.joints[0].isedge = True
        self.joints[-1].isedge = True
        return
    
    def simpleforces(self) -> None:
        j = self.joints
        for i in range(0, len(j)):
            j[i].applygravity()
            # j[i].checkfloor()
            # j[i].applyfriction()
        return
    
    def rigidity(self) -> None:
        j = self.joints
        for i in range(0, len(j)):
            if(i > 1):
                j[i].computerigidity(j[i - 2])
                j[i - 2].computerigidity(j[i])
        for i in range(0, len(j)):
            j[i].applyrigidity()
        return
    
    def tension(self) -> None:
        j = self.joints
        for _ in range(0, len(j)):
            for i in range(0, len(j)):
                if(i != 0):
                    j[i].computetension(j[i - 1])
                    j[i - 1].computetension(j[i])
            for i in range(0, len(j)):
                j[i].applytension()
        return
    
    def collisions(self, shapes:list) -> None:
        j = self.joints
        for i in j:
            for _ in range(3): 
                # 3 is totally arbitrary but you will rarely encounter more than 3 segments at once
                for k in shapes:
                    md = -1
                    seg = None
                    for s in k.segments:
                        if(s.intersect((i.x, i.y), (i.x + i.speedx, i.y + i.speedy))):
                            u, v = s.intersection((i.x, i.y), (i.x + i.speedx, i.y + i.speedy))
                            d = (u - i.x) ** 2 + (v - i.y) ** 2
                            if(d < md or md == -1):
                                md = d
                                seg = s
                    if(md != -1):
                        i.applyreaction(seg)
        return
    
    def preventnoclip(self, shapes:list) -> None:
        for j in self.joints:
            for k in shapes:
                c = 0
                for s in k.segments:
                    if(s.intersect((j.x, j.y), (INFINITY, j.y))):
                        c += 1
                if(c & 1):
                    d = -1
                    (u, v) = (0, 0)
                    for s in k.segments:
                        (up, vp) = s.projection((j.x, j.y))
                        dp = (up - j.x) ** 2 + (vp - j.y) ** 2
                        if(dp < d or d == -1):
                            d = dp
                            (u, v) = (up, vp)
                    (j.x, j.y) = (u, v)
        return
    
    def move(self) -> None:
        j = self.joints
        for i in range(0, len(j)):
            j[i].move()
        return

    def update(self, shapes:list, *args) -> None:
        self.simpleforces()
        self.rigidity()
        self.tension()
        self.collisions(shapes)
        self.move()
        self.preventnoclip(shapes)
        return
    
    def draw(self, *args) -> None:
        j = self.joints
        for i in range(len(j)):
            if(i != 0):
                j[i].draw(j[i - 1].x, j[i - 1].y)
            else:
                j[i].draw(j[i].x, j[i].y)
        return

class Segment:
    def __init__(self, A:tuple, B:tuple) -> None:
        self.A = A
        self.B = B
        self.nextA = self.A
        self.nextB = self.B

    @staticmethod
    def _intersect(A, B, C, D) -> bool:
        # Stolen from https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/ with a little spice added
        def collinear(A, B, C, D):
            # Cross product
            return (B[0] - A[0]) * (D[1] - C[1]) - (B[1] - A[1]) * (D[0] - C[0]) == 0
        # Apparently, ccw = counter clockwise
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        return (ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)) and not collinear(A,B,C,D)

    def intersect(self, C, D) -> bool:
        return self._intersect(self.A, self.B, C, D)
    
    @staticmethod
    def _projection(A, B, C) -> tuple:
        # Stolen from ChatGPT 3.5
        def dot_product(v1, v2):
            return v1[0] * v2[0] + v1[1] * v2[1]

        def vector_subtraction(v1, v2):
            return (v1[0] - v2[0], v1[1] - v2[1])

        def scalar_multiplication(scalar, vector):
            return (scalar * vector[0], scalar * vector[1])
        
        AB = vector_subtraction(B, A)
        AC = vector_subtraction(C, A)
        dot_AB_AC = dot_product(AB, AC)
        length_AB_squared = dot_product(AB, AB)
        scalar_projection_factor = dot_AB_AC / length_AB_squared
        P = scalar_multiplication(scalar_projection_factor, AB)
        projection_point = (P[0] + A[0], P[1] + A[1])
        
        return projection_point

    def projection(self, C) -> tuple:
        return self._projection(self.A, self.B, C)
    
    def intersection(self, C, D) -> tuple:
        # Also stolen from GPT 3.5 but refactored
        p = self.A
        r = (self.B[0] - self.A[0], self.B[1] - self.A[1])
        q = C
        s = (D[0] - C[0], D[1] - C[1])
        det = r[0] * s[1] - r[1] * s[0]
        t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / det
        return (p[0] + t * r[0], p[1] + t * r[1])
    
    def computemove(self, A, B, j:Joint) -> None:
        # Check if point is in the polygon
        x = self._intersect(A, B, (j.x, j.y), (INFINITY, j.y))
        y = self._intersect(self.A, self.B, (j.x, j.y), (INFINITY, j.y))
        z = self._intersect(self.A, A, (j.x, j.y), (INFINITY, j.y))
        t = self._intersect(self.B, B, (j.x, j.y), (INFINITY, j.y))
        c = (x + y + z + t) & 1 # Is c odd ? (the LSB is 1)
        # Make a projection of the point on the new segment
        if(c):
            prevpx = j.x
            prevpy = j.y
            (j.x, j.y) = self._projection(A, B, (j.x, j.y))
            if(j.x - prevpx != 0):
                # Adding small padding to avoid noclipping through the segment
                j.x += (j.x - prevpx) / abs(j.x - prevpx) / 10
                j.speedx += j.x - prevpx
            if(j.y - prevpy != 0):
                j.y += (j.y - prevpy) / abs(j.y - prevpy) / 10
                j.speedy += j.y - prevpy
        return
    
    def applymove(self, A, B) -> None:
        self.A = A
        self.B = B
        return
    
    def move(self, b:Blob) -> None:
        for j in b.joints:
            self.computemove(self.nextA, self.nextB, j)
        self.applymove(self.nextA, self.nextB)
        return
    
    def draw(self) -> None:
        pygame.draw.line(screen, "black", self.A, self.B, 10)
        return

class Point:
    def __init__(self, coordinates:tuple) -> None:
        # Fixed coordinates I.E at pos O angle 0
        self.fx = coordinates[0]
        self.fy = coordinates[1]
        # Actual coordinates of the point
        self.x = self.fx
        self.y = self.fy
        # Coordinates of the parent shape
        self.absx = 0
        self.absy = 0
        self.angle = 0
        return
    
    def move(self, x:float, y:float) -> None:
        self.segA.nextA = (self.x + x, self.y + y)
        self.segB.nextB = (self.x + x, self.y + y)
        self.absx = x
        self.absy = y
        return
    
    def rotate(self, angle:float) -> None:
        self.x = self.fx * math.cos(angle) - self.fy * math.sin(angle)
        self.y = self.fy * math.cos(angle) + self.fx * math.sin(angle)
        self.move(self.absx, self.absy)
        return

    def setsegA(self, segment:Segment) -> None:
        self.segA = segment
        return
    
    def setsegB(self, segment:Segment) -> None:
        self.segB = segment
        return

class Shape:
    def __init__(self, points:list = []) -> None:
        self.angle = 0
        self.x = 0
        self.y = 0
        self.points:list[Point] = []
        for p in points:
            self.points.append(Point(p))
        self.segments:list[Segment] = []
        for i in range(len(self.points)):
            s = Segment(points[i - 1], points[i])
            self.segments.append(s)
            self.points[i - 1].setsegA(s)
            self.points[i].setsegB(s)
        return

    def move(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
        for p in self.points:
            p.move(self.x, self.y)
        for s in self.segments:
            s.move(b)
        return

    def rotate(self, angle:float) -> None:
        self.angle = angle
        for p in self.points:
            p.rotate(self.angle)
        for s in self.segments:
            s.move(b)
        return
    
    def draw(self, *args):
        for s in self.segments:
            s.draw()
        return

b = Blob()

s = Shape([
    (0, 0),
    (30, 20),
    (200, 20),
    (230, 0),
    (245, 5),
    (250, 20),
    (240, 30),
    (215, 45),
    (15, 45),
    (-10, 30),
    (-20, 20),
    (-15, 5),
])
# floor = Shape([(0, 0), (1280, 0)])
# floor.move(0, 700)
s.move(320, 200)
# sg = [
#     # Segment((350, 325), (400, 350)),
#     Segment((400, 350), (600, 350)),
#     # Segment((650, 325), (600, 350))
# ]
# j.append(Join(642, 310, 50))
for i in range(20):
    b.addjoint(Joint(380 + i * 8, 100, 8))
b.fix()

score=Score()

image = pygame.image.load("fondcrepe.jpg")
size= (1280,1280)
image = pygame.transform.scale(image, size)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_UP]):
        s.move(s.x, s.y - 3)
    if(keys[pygame.K_DOWN]):
        s.move(s.x, s.y + 3)
    if(keys[pygame.K_LEFT]):
        s.move(s.x - 3, s.y)
    if(keys[pygame.K_RIGHT]):
        s.move(s.x + 3, s.y)
    if(keys[pygame.K_SPACE]):
        if s.angle<=angle:
            s.rotate(s.angle + .05)
        pressed=True
    elif pressed:
        if s.angle>=-angle:
            s.rotate(s.angle - .1)
        else:
            launched=True
            pressed=False
    elif launched:
        if s.angle<=-0.05:
            s.rotate(s.angle + .05)
        else:
            launched=False

    if(keys[pygame.K_r]):
        b.joints=[]
        for i in range(20):
            b.addjoint(Joint(s.x + 35 + i * 8, s.y-20, 8))
        b.fix()
        score.score=0

    b.update([s, ])


    screen.blit(image,(0,-200))

    # floor.draw()
    s.draw()
    b.draw()
    score.draw(b)
    pygame.display.flip()
    dt = clock.tick(60)