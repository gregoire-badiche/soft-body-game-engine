import math
from segment import Segment

from constants import *

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