import pygame
from joint import Joint

from constants import *

class Segment:
    def __init__(self, A:tuple, B:tuple) -> None:
        self.A = A
        self.B = B
        self.nextA = self.A
        self.nextB = self.B
        self.prevA = self.A
        self.prevB = self.B
        self.hasmoved = True

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
        self.prevA = self.A
        self.prevB = self.B
        self.A = A
        self.B = B
        self.hasmoved = True
        return
    
    def move(self, b) -> None:
        for j in b.joints:
            self.computemove(self.nextA, self.nextB, j)
        self.applymove(self.nextA, self.nextB)
        return
    
    def update(self) -> None:
        if(self.hasmoved):
            self.hasmoved = False
        else:
            self.prevA = self.A
            self.prevB = self.B
        return

    def draw(self) -> None:
        pygame.draw.line(screen, "black", self.A, self.B, 10)
        return