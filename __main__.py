import pygame
import io
import os
import random

from globalconst import *
from gameobjects import *
from bitmapfont import BitmapFont

pygame.display.init()

player = GameObject(0,0)

if FULLSCREEN:
    window = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode((WIN_W, WIN_H), 0)

screen = pygame.Surface((SCR_W, SCR_H))

clock = pygame.time.Clock()

pygame.mixer.init(44100)
pygame.joystick.init()

for i in range(pygame.joystick.get_count()):
    pygame.joystick.Joystick(i).init()

pygame.mouse.set_visible(False)

font = BitmapFont('gfx/heimatfont.png', scr_w=SCR_W, scr_h=SCR_H, colors=[(255,255,255), (240,0,240)])


def toggleFullscreen():
    global FULLSCREEN, window
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        window = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode((WIN_W, WIN_H), 0)

def controls():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False

            if e.key == pygame.K_LEFT:
                player.moveLeft()
            if e.key == pygame.K_RIGHT:
                player.moveRight()
            if e.key == pygame.K_UP:
                player.moveUp()
            if e.key == pygame.K_DOWN:
                player.moveDown()

            if e.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_LALT or mods & pygame.KMOD_RALT:
                    toggleFullscreen()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                player.stopLeft()
            if e.key == pygame.K_RIGHT:
                player.stopRight()
            if e.key == pygame.K_UP:
                player.stopUp()
            if e.key == pygame.K_DOWN:
                player.stopDown()

            if e.key == pygame.K_F11:
                global FPS
                if FPS == 20:
                    FPS = 60
                else:
                    FPS = 20

            if e.key == pygame.K_F12:
                global DEBUG_MODE
                DEBUG_MODE = not DEBUG_MODE

        if e.type == pygame.JOYAXISMOTION:
            if e.axis == 0:
                if e.value < -JOY_DEADZONE:
                    player.moveLeft()
                elif e.value > JOY_DEADZONE:
                    player.moveRight()
                else:
                    if player.xdir < 0:
                        player.stopLeft()
                    if player.xdir > 0:
                        player.stopRight()

            if e.axis == 1:
                if e.value < -JOY_DEADZONE:
                    player.moveUp()
                elif e.value > JOY_DEADZONE:
                    player.moveDown()
                else:
                    if player.ydir < 0:
                        player.stopUp()
                    if player.ydir > 0:
                        player.stopDown()

        if e.type == pygame.JOYBUTTONDOWN:
            if e.button == 1:
                player.doJump()
            elif e.button == 0:
                player.interact()

        if e.type == pygame.JOYBUTTONUP:
            if e.button == 1:
                player.cancelJump()

    return True

def render():
    screen.fill((0, 0, 0))
    font.drawText(screen, 'SNAKE SOCCER', 0, 0, fgcolor=(255,255,255))#, bgcolor=(0,0,0))


def update():
    pass




tick = 0
running = True

while running:
    tick += 1

    render()

    pygame.transform.scale(screen, window.get_size(), window)
    pygame.display.flip()

    cont = controls()

    if not cont:
        running = False

    update()

    clock.tick(FPS)


