from constants import *
from segment import Segment

class Blob:
    def __init__(self, joints:list = []) -> None:
        self.joints = joints
        return

    def __len__(self) -> int:
        return len(self.joints)

    def get_joints(self):
        return self.joints

    def addjoint(self, joint) -> int:
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

    def update(self, shapes:list, *args) -> bool:
        self.simpleforces()
        self.rigidity()
        self.tension()
        self.collisions(shapes)
        res = self.checkflip()
        self.move()
        self.preventnoclip(shapes)
        return res
    
    def checkflip(self) -> bool:
        j1 = self.joints[0]
        j2 = self.joints[-1]
        return Segment._intersect(
            (j1.x, j1.y),
            (j1.x + j1.speedx, j1.y + j1.speedy),
            (j2.x + j2.speedx, INFINITY),
            (j2.x + j2.speedx, -1 * INFINITY)
        ) or Segment._intersect(
            (j1.x, j1.y),
            (j1.x + j1.speedx, j1.y + j1.speedy),
            (j2.x, INFINITY),
            (j2.x, -1 * INFINITY)
        )

    def draw(self, *args) -> None:
        j = self.joints
        for i in range(len(j)):
            if(i != 0):
                j[i].draw(j[i - 1].x, j[i - 1].y)
            else:
                j[i].draw(j[i].x, j[i].y)
        return
