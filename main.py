#!/usr/bin/env python3

import pygame
import sys
import math
import time
import webbrowser

from button import Button
from score import Score
from joint import Joint
from blob import Blob
from shape import Shape

from constants import *

BG = pygame.image.load("ressources/Background.jpg")
BG = pygame.transform.scale(BG, (1280, 720))
BG = pygame.transform.flip(BG, True, False)

pygame.mixer.init()
pygame.mixer.music.load("ressources/musique.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.06)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("ressources/VeniteAdoremus-rgRBA.ttf", size)

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

        OPTIONS_TEXT = get_font(55).render("How to play", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        SCORE_TEXT = get_font(35).render("Make the highest score by flipping your pan !", True, "Black")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(645,550))
        screen.blit(SCORE_TEXT,SCORE_RECT)

        
        OPTIONS_COMMANDS = pygame.image.load("ressources/commands.png")
        COMMANDS_RECT = OPTIONS_COMMANDS.get_rect(center=(640,350))
        screen.blit(OPTIONS_COMMANDS,COMMANDS_RECT)


        OPTIONS_BACK = Button(image=None, pos=(130, 665), 
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

def credits():
     while True:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        CREDITS_TEXT = get_font(55).render("Meet our Development team !", True, "Black")
        CREDITS_RECT = CREDITS_TEXT.get_rect(center=(640, 150))
        screen.blit(CREDITS_TEXT, CREDITS_RECT)

        
        BUTTON_OSCAR = Button(image= pygame.transform.scale (pygame.image.load("ressources/oscar.jpg"), (200,200) ), pos=(200,350),
                               text_input="", font=get_font(65), base_color="#d7fcd4", hovering_color="White" )
        OSCAR_TEXT = get_font(15).render("Oscar Masdupuy", True, "Black")
        OSCAR_RECT = OSCAR_TEXT.get_rect(center=(200,475))
        screen.blit(OSCAR_TEXT,OSCAR_RECT)
        
        BUTTON_VALENTIN = Button(image= pygame.transform.scale (pygame.image.load("ressources/valentin.jpg"), (200,200) ), pos=(422,350),
                               text_input="", font=get_font(65), base_color="#d7fcd4", hovering_color="White" )
        VALENTIN_TEXT = get_font(15).render("Valentin Auffray", True, "Black")
        VALENTIN_RECT = VALENTIN_TEXT.get_rect(center=(422,475))
        screen.blit(VALENTIN_TEXT,VALENTIN_RECT)
        
        BUTTON_GREGOIRE = Button(image= pygame.transform.scale (pygame.image.load("ressources/gregoire.png"), (200,200) ), pos=(645,350),
                               text_input="", font=get_font(65), base_color="#d7fcd4", hovering_color="White" )
        GREGOIRE_TEXT = get_font(15).render("Grégoire Badiche", True, "Black")
        GREGOIRE_RECT = GREGOIRE_TEXT.get_rect(center=(645,475))
        screen.blit(GREGOIRE_TEXT,GREGOIRE_RECT)
        
        BUTTON_JUDE = Button(image= pygame.transform.scale (pygame.image.load("ressources/jude.jpg"), (200,200) ), pos=(867,350),
                               text_input="", font=get_font(65), base_color="#d7fcd4", hovering_color="White" )
        JUDE_TEXT = get_font(15).render("Jude Guehl", True, "Black")
        JUDE_RECT = JUDE_TEXT.get_rect(center=(867,475))
        screen.blit(JUDE_TEXT,JUDE_RECT)
        
        BUTTON_SAMY = Button(image= pygame.transform.scale (pygame.image.load("ressources/samy.jpg"), (200,200) ), pos=(1090,350),
                               text_input="", font=get_font(65), base_color="#d7fcd4", hovering_color="White" )
        SAMY_TEXT = get_font(15).render("Samy Gharnaout", True, "Black")
        SAMY_RECT = SAMY_TEXT.get_rect(center=(1090,475))
        screen.blit(SAMY_TEXT,SAMY_RECT)  

        for button in [BUTTON_OSCAR,BUTTON_VALENTIN,BUTTON_JUDE,BUTTON_GREGOIRE,BUTTON_SAMY]:
            button.changeColor(CREDITS_MOUSE_POS)
            button.update(screen)


        CREDITS_BACK = Button(image=None, pos=(130, 665), 
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="#b68f40")

        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    main_menu()
                if BUTTON_OSCAR.checkForInput(CREDITS_MOUSE_POS):
                    webbrowser.open("https://www.linkedin.com/in/oscar-masdupuy-375246250/")
                if BUTTON_VALENTIN.checkForInput(CREDITS_MOUSE_POS):
                    webbrowser.open("https://www.linkedin.com/in/valentin-auffray-024230251/")
                if BUTTON_GREGOIRE.checkForInput(CREDITS_MOUSE_POS):
                    webbrowser.open("https://www.linkedin.com/in/gregoire-badiche/")
                if BUTTON_JUDE.checkForInput(CREDITS_MOUSE_POS):
                    webbrowser.open("https://www.linkedin.com/in/jude-guehl-366932294/")
                if BUTTON_SAMY.checkForInput(CREDITS_MOUSE_POS):
                    webbrowser.open("https://www.linkedin.com/in/samy-gharnaout/")
                

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
        CREDITS_BUTTON = Button(image=pygame.image.load("ressources/Play-Rect.png"),pos=(1125,650),
                            text_input="Credits", font=get_font(50), base_color="#d7fcd4", hovering_color="White" )

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, CREDITS_BUTTON]:
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
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_over():
    while True:
        pygame.mixer.music.stop()
        screen.fill("Black")
        
        GAMEOVER_MOUSE_POS = pygame.mouse.get_pos()

        GAMEOVER_TEXT = get_font(55).render("GAME OVER", True, "Red")
        GAMEOVER_RECT = GAMEOVER_TEXT.get_rect(center=(640, 360))
        screen.blit(GAMEOVER_TEXT, GAMEOVER_RECT)


        GAMEOVER_BACK = Button(image=None, pos=(130, 665), 
                            text_input="BACK", font=get_font(55), base_color="White", hovering_color="Red")
        

        GAMEOVER_BACK.changeColor(GAMEOVER_MOUSE_POS)
        GAMEOVER_BACK.update(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAMEOVER_BACK.checkForInput(GAMEOVER_MOUSE_POS):
                    pygame.mixer.music.play(-1)
                    main_menu()

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
            game_over()
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
