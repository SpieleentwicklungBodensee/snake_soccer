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
from ball import Ball
from playerobject import *

import network

playerId = 0    # 0 = worm, other id = player

parser = argparse.ArgumentParser()
parser.add_argument('--connect')
parser.add_argument('--port', type=int, default=2000)
parser.add_argument('--host', action='store_true')
parser.add_argument('--id', type=int, default=0)    # only for testing
args = parser.parse_args()

playerId = args.id  # only for testing

net = None
if args.connect is not None:
    net = network.connect(args.connect, args.port)
    playerId = 1    # TODO use id received from host
elif args.host:
    net = network.serve(args.port)


pygame.display.init()

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
         '3': pygame.image.load('gfx/player3.png'),
         'o': pygame.image.load('gfx/ball.png')
         }



worm   = Worm(math.floor(len(level[0])/2),math.floor(len(level)/2),TILE_W,TILE_H)
ball   = Ball(math.floor(SCR_W/4),math.floor(SCR_H/2),'o')
player = Player(4, 4, '1')

players = [worm, player]
ownPlayer = players[playerId]


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
                ownPlayer.moveLeft()
            if e.key == pygame.K_RIGHT:
                ownPlayer.moveRight()
            if e.key == pygame.K_UP:
                ownPlayer.moveUp()
            if e.key == pygame.K_DOWN:
                ownPlayer.moveDown()

            if e.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_LALT or mods & pygame.KMOD_RALT:
                    toggleFullscreen()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                ownPlayer.stopLeft()
            if e.key == pygame.K_RIGHT:
                ownPlayer.stopRight()
            if e.key == pygame.K_UP:
                ownPlayer.stopUp()
            if e.key == pygame.K_DOWN:
                ownPlayer.stopDown()

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
                    ownPlayer.moveLeft()
                elif e.value > JOY_DEADZONE:
                    ownPlayer.moveRight()
                else:
                    if ownPlayer.xdir < 0:
                        ownPlayer.stopLeft()
                    if ownPlayer.xdir > 0:
                        ownPlayer.stopRight()

            if e.axis == 1:
                if e.value < -JOY_DEADZONE:
                    ownPlayer.moveUp()
                elif e.value > JOY_DEADZONE:
                    ownPlayer.moveDown()
                else:
                    if ownPlayer.ydir < 0:
                        ownPlayer.stopUp()
                    if ownPlayer.ydir > 0:
                        ownPlayer.stopDown()

        if e.type == pygame.JOYBUTTONDOWN:
            pass

        if e.type == pygame.JOYBUTTONUP:
            pass

    return True

def render():
    screen.fill((0, 128, 0))
    font.drawText(screen, 'SNAKE SOCCER!', 2, 2, fgcolor=(255,255,255))#, bgcolor=(0,0,0))

    # render level
    for y in range(LEV_H):
        for x in range(LEV_W):
            if level[y][x] == '#':
                screen.blit(tiles['#'], (x * TILE_W, y * TILE_H))

    # render players
    for p in players:
        p.draw(screen, tiles)

    ball.draw(screen, tiles)

def update():
    global players
    for p in players:
        p.update()

    ball.update()

    if net is not None:
        players = net.update(players)
        ownPlayer = players[playerId]


tick = 0
running = True

try:
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

finally:
    if net is not None:
        net.stop()

    pygame.quit()
