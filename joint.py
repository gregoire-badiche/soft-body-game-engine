import pygame
import math
from constants import *

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
        pygame.draw.circle(screen, "darkgoldenrod1", (self.x, self.y), 5)
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
        self.speedx = f[0] - self.x + (f[0] - self.x - self.speedx) / d - (f[0] - e[0] - s.A[0] + s.prevA[0]) * F
        self.speedy = f[1] - self.y + (f[1] - self.y - self.speedy) / d - (f[1] - e[1]) * F
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