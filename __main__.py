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


ownId = 0    # 0 = worm, 1 = ball, rest = players
playerColor = 1
actions = []
objects = {}

parser = argparse.ArgumentParser()
parser.add_argument('--connect')
parser.add_argument('--port', type=int, default=2000)
parser.add_argument('--host', action='store_true')
args = parser.parse_args()

net = None
if args.connect is not None:
    net = network.connect(args.connect, args.port)
    ownId = int(random.random() * 1000000) + 2       # 0 and 1 are reserved
    actions.append(('create-player', ownId))
    print('i am player with id=', ownId)
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
         '10': pygame.image.load('gfx/player1.png'),
         '11': pygame.image.load('gfx/player1-walk1.png'),
         '12': pygame.image.load('gfx/player1-walk2.png'),
         '20': pygame.image.load('gfx/player2.png'),
         '21': pygame.image.load('gfx/player2-walk1.png'),
         '22': pygame.image.load('gfx/player2-walk2.png'),
         '30': pygame.image.load('gfx/player3.png'),
         '31': pygame.image.load('gfx/player3-walk1.png'),
         '32': pygame.image.load('gfx/player3-walk2.png')
         }



worm   = Worm(math.floor(len(level[0])/2),math.floor(len(level)/2),TILE_W,TILE_H)
ball   = Ball(math.floor(SCR_W/4),math.floor(SCR_H/2),TILE_W,TILE_H)

objects[0] = worm
objects[1] = ball


def toggleFullscreen():
    global FULLSCREEN, window
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        window = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode((WIN_W, WIN_H), 0)

def createPlayer(objId):
    global playerColor, objects
    newPlayer = Player(TILE_W * 2, TILE_H * 2, playerColor)
    playerColor += 1
    objects[objId] = newPlayer
    print('created player with id=', objId)

def controls():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False

            if e.key == pygame.K_LEFT:
                actions.append(('move-left', ownId))
            if e.key == pygame.K_RIGHT:
                actions.append(('move-right', ownId))
            if e.key == pygame.K_UP:
                actions.append(('move-up', ownId))
            if e.key == pygame.K_DOWN:
                actions.append(('move-down', ownId))

            if e.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_LALT or mods & pygame.KMOD_RALT:
                    toggleFullscreen()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                actions.append(('stop-left', ownId))
            if e.key == pygame.K_RIGHT:
                actions.append(('stop-right', ownId))
            if e.key == pygame.K_UP:
                actions.append(('stop-up', ownId))
            if e.key == pygame.K_DOWN:
                actions.append(('stop-down', ownId))

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
                    actions.append(('move-left', ownId))
                elif e.value > JOY_DEADZONE:
                    actions.append(('move-right', ownId))
                else:
                    if ownPlayer.xdir < 0:
                        actions.append(('stop-left', ownId))
                    if ownPlayer.xdir > 0:
                        actions.append(('stop-right', ownId))

            if e.axis == 1:
                if e.value < -JOY_DEADZONE:
                    actions.append(('move-up', ownId))
                elif e.value > JOY_DEADZONE:
                    actions.append(('move-down', ownId))
                else:
                    if ownPlayer.ydir < 0:
                        actions.append(('stop-up', ownId))
                    if ownPlayer.ydir > 0:
                        actions.append(('stop-down', ownId))

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
    for obj in objects.values():
        obj.draw(screen, tiles)

def update():
    global actions, objects, ownPlayer

    for obj in objects.values():
        obj.update()

    if net is not None:
        objects, actions = net.update(objects, actions)
        ownPlayer = objects.get(ownId)

    for action, objId in actions:
        if action == 'create-player':
            createPlayer(objId)
            continue

        obj = objects.get(objId)

        if not obj:
            continue

        if action == 'move-left':
            obj.moveLeft()
        elif action == 'move-right':
            obj.moveRight()
        elif action == 'move-up':
            obj.moveUp()
        elif action == 'move-down':
            obj.moveDown()
        elif action == 'stop-left':
            obj.stopLeft()
        elif action == 'stop-right':
            obj.stopRight()
        elif action == 'stop-up':
            obj.stopUp()
        elif action == 'stop-down':
            obj.stopDown()

    actions = []


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
