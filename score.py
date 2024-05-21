import pygame
from time import perf_counter
from datetime import date
import csv

from constants import *

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

    def update(self, flip) -> None:
        if(flip):
            self.tac = round(perf_counter())
            if(self.tac - self.tic > .1):
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
    
    def draw(self, flip) -> None:
        self.update(flip)
        screen.blit(self.rendred, self.coordinates)
        return
    
    def get_font(self, size):
        return pygame.font.Font("ressources/fonts/VeniteAdoremus-rgRBA.ttf", size)
    
    def edit_chart(self, name='Jude test') -> None:
        with open("ressources/scores.csv",'a',newline='') as csvfile:
            today=date.today()
            today = today.strftime("%d/%m/%y")
            scores=csv.writer(csvfile, delimiter=',')
            scores.writerow([name,str(self.score), today])
        return 

    def read(self) -> list:
        with open("ressources/scores.csv", newline='') as csvfile:
            scores = csv.reader(csvfile, delimiter=',')
            scores=[tuple(row) for row in scores]
            scores.sort(key=lambda tup: tup[1])
        return scores[:-1]