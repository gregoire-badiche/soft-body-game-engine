import pygame
from segment import Segment
from point import Point
from blob import Blob

from constants import *

class Shape:
    def __init__(self, b:Blob, points:list = []) -> None:
        self.angle = 0
        self.x = 0
        self.y = 0
        self.b = b
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
            s.move(self.b)
        return

    def rotate(self, angle:float) -> None:
        self.angle = angle
        for p in self.points:
            p.rotate(self.angle)
        for s in self.segments:
            s.move(self.b)
        return
    
    def draw(self, *args):
        p = []
        for s in self.segments:
            s.update()
        for po in self.points:
            p.append((po.absx + po.x, po.absy + po.y))
        pygame.draw.polygon(screen, "black", p)
        return