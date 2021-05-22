import pygame
import argparse
import io
import os
import random
import math

from globalconst import *
from gameobjects import *
from bitmapfont import BitmapFont
from worm import Worm

import network

parser = argparse.ArgumentParser()
parser.add_argument('--connect')
parser.add_argument('--port', type=int, default=2000)
parser.add_argument('--host', action='store_true')
args = parser.parse_args()

net = None
if args.connect is not None:
    net = network.connect(args.connect, args.port)
elif args.host:
    net = network.serve(args.port)


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


level = ['########################################',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                               ###    #',
         '#                                 #    #',
         '#                                 #    #',
         '#                                 #    #',
         '#                                 #    #',
         '#                               ###    #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '#                                      #',
         '########################################',
         ]

tiles = {'#': pygame.image.load('gfx/wall.png'),
         'H': pygame.image.load("gfx/worm_head.png"),
         'B': pygame.image.load("gfx/worm_body.png"),
         '1': pygame.image.load('gfx/player1.png'),
         '2': pygame.image.load('gfx/player2.png'),
         '3': pygame.image.load('gfx/player3.png')
         }



worm   = Worm(math.floor(len(level[0])/2),math.floor(len(level)/2),TILE_W,TILE_H)

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
                worm.moveLeft()
            if e.key == pygame.K_RIGHT:
                player.moveRight()
                worm.moveRight()
            if e.key == pygame.K_UP:
                player.moveUp()
                worm.moveUp()
            if e.key == pygame.K_DOWN:
                player.moveDown()
                worm.moveDown()

            if e.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_LALT or mods & pygame.KMOD_RALT:
                    toggleFullscreen()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                player.stopLeft()
                worm.stopLeft()
            if e.key == pygame.K_RIGHT:
                player.stopRight()
                worm.stopRight()
            if e.key == pygame.K_UP:
                player.stopUp()
                worm.stopUp()
            if e.key == pygame.K_DOWN:
                player.stopDown()
                worm.stopDown()

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
    screen.fill((0, 128, 0))
    font.drawText(screen, 'SNAKE SOCCER!', 2, 2, fgcolor=(255,255,255))#, bgcolor=(0,0,0))

    # render level
    for y in range(LEV_H):
        for x in range(LEV_W):
            if level[y][x] == '#':
                screen.blit(tiles['#'], (x * TILE_W, y * TILE_H))

    # render worm
    worm.draw(screen,tiles)

def update():
    worm.update()
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


if net is not None:
    net.stop()
