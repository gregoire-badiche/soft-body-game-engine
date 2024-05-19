#!/usr/bin/env python3

import pygame
import sys
import math
import time
from random import randint
from time import perf_counter, sleep

from button import Button
from score import Score
from joint import Joint
from blob import Blob
from segment import Segment
from point import Point
from shape import Shape

from constants import *

BG = pygame.image.load("ressources/Background.jpg")
BG = pygame.transform.scale(BG, (1280, 720))
BG = pygame.transform.flip(BG, True, False)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("ressources/VeniteAdoremus-rgRBA.ttf", size)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

pygame.display.set_caption("Menu")

running = True
average:int = 2 #average distance between the first and the last joint


def crepe(x, y):
    a = Blob()
    a.joints = []
    for i in range(20):
        a.addjoint(Joint(x + i * 8, y, 8))
    a.fix()
    return a

def poele(x, y, b):
    s = Shape(b, [
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
    s.move(x, y)
    return s

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(55).render("Welcome to the COMMANDS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        
        OPTIONS_COMMANDS = pygame.image.load("ressources/commands.png")
        COMMANDS_RECT = OPTIONS_COMMANDS.get_rect(center=(640,350))
        screen.blit(OPTIONS_COMMANDS,COMMANDS_RECT)


        OPTIONS_BACK = Button(image=None, pos=(160, 650), 
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="#b68f40")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("BRETON SIMULATOR 2024", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("ressources/Play-Rect.png"), pos=(180, 250), 
                            text_input="Play", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("ressources/Options-Rect.png"), pos=(290, 400), 
                            text_input="Commands", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("ressources/Play-Rect.png"), pos=(180, 550), 
                            text_input="Quit", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
def main():
    running = True
    c = crepe(580, 100)

    s = poele(520, 500, c)

    launched = False
    pressed = False
    angle = math.pi / 6
    running = True
    
    score = Score()
    super_speed_active = False
    super_speed_start_time = 0
    super_speed_duration = 3  

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 0

        keys = pygame.key.get_pressed()
        current_time = time.time()
        
        move_speed = 3
        super_move_speed = 7
        
        # Check if the chosen key is pressed
        if keys[pygame.K_c]:
            super_speed_active = True
            super_speed_start_time = current_time

        
        if super_speed_active and (current_time - super_speed_start_time > super_speed_duration):
            super_speed_active = False

        
        current_speed = super_move_speed if super_speed_active else move_speed

        if keys[pygame.K_UP]:
            s.move(s.x, s.y - current_speed)
        
        if keys[pygame.K_DOWN]:
            s.move(s.x, s.y + current_speed)

        if keys[pygame.K_LEFT]:
            s.move(s.x - current_speed, s.y)

        if keys[pygame.K_RIGHT]:
            s.move(s.x + current_speed, s.y)

        if keys[pygame.K_SPACE]:
            if s.angle <= angle:
                s.rotate(s.angle + .05)
            pressed = True
        elif pressed:
            if s.angle >= -angle:
                s.rotate(s.angle - .1)
            else:
                launched = True
                pressed = False
        elif launched:
            if s.angle <= -0.05:
                s.rotate(s.angle + .05)
            else:
                launched = False

        flip = c.update([s, ])

        if c.joints[0].y > 1000 and c.joints[-1].y > 1000:
            running = False
            c.joints = []
            score = 0
            return 1

        image = pygame.image.load("ressources/fondcrepe.jpg")
        size = (1280, 1280)
        image = pygame.transform.scale(image, size)
        screen.blit(image, (0, -200))

        s.draw()
        c.draw()
        score.draw(flip)
        pygame.display.flip()
        dt = clock.tick(60)

x = True
while x:
    main_menu()
