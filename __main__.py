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
from bird import Bird
from playerobject import *

from gamestate import GameState
import sound

import network


ownId = -1    # -1 = worm, -2 = ball, rest = players
playerColor = 0
actions = []
objects = {}

parser = argparse.ArgumentParser()
parser.add_argument('--connect')
parser.add_argument('--port', type=int, default=2000)
parser.add_argument('--host', action='store_true')
parser.add_argument('--nosnake', action='store_true')
parser.add_argument('--level', type=str, default='LEV1')
args = parser.parse_args()

net = None
if args.connect is not None:
    net = network.connect(args.connect, args.port)
    ownId = int(random.random() * 1000000)
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


tiles = {'#': pygame.image.load('gfx/wall.png'),
         '.': pygame.image.load('gfx/goal.png'),
         'H': pygame.image.load("gfx/worm_head.png"),
         'B': pygame.image.load("gfx/worm_body.png"),
         'o': pygame.image.load('gfx/ball.png'),
         'v': pygame.image.load('gfx/bird.png'),
         '10': pygame.image.load('gfx/player1.png'),
         '11': pygame.image.load('gfx/player1-walk1.png'),
         '12': pygame.image.load('gfx/player1-walk2.png'),
         '20': pygame.image.load('gfx/player2.png'),
         '21': pygame.image.load('gfx/player2-walk1.png'),
         '22': pygame.image.load('gfx/player2-walk2.png'),
         '30': pygame.image.load('gfx/player3.png'),
         '31': pygame.image.load('gfx/player3-walk1.png'),
         '32': pygame.image.load('gfx/player3-walk2.png'),
         '40': pygame.image.load('gfx/player4.png'),
         '41': pygame.image.load('gfx/player4-walk1.png'),
         '42': pygame.image.load('gfx/player4-walk2.png'),
         '50': pygame.image.load('gfx/player5.png'),
         '51': pygame.image.load('gfx/player5-walk1.png'),
         '52': pygame.image.load('gfx/player5-walk2.png'),
         }


sound.loadSound('whistle', 'snd/trillerpfeife.wav')
sound.loadSound('kick', 'snd/kick.wav')


gamestate = GameState(args.level)

def toggleFullscreen():
    global FULLSCREEN, window
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        window = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode((WIN_W, WIN_H), 0)

def createPlayer(objId):
    global playerColor, gamestate

    # create worm for first joined player if host doesn't want to be a worm (TODO this is a bit ugly, code-wise)
    if objId != -1:
        if net is not None and net.isHost():
            if args.nosnake:
                if not gamestate.getWorms():
                    worm = Worm(math.floor(LEV_W/2),math.floor(LEV_H/2))
                    gamestate.objects[objId] = worm
                    print('created worm for player id=', objId)
                    return

    # create ordinary player
    newPlayer = Player(TILE_W * 2, TILE_H * 2, playerColor)
    playerColor += 1
    gamestate.objects[objId] = newPlayer
    print('created player with id=', objId)

def controls():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False

            if e.key in KEYS_LEFT:
                actions.append(('move-left', ownId))
            if e.key in KEYS_RIGHT:
                actions.append(('move-right', ownId))
            if e.key in KEYS_UP:
                actions.append(('move-up', ownId))
            if e.key in KEYS_DOWN:
                actions.append(('move-down', ownId))

            if e.key in KEYS_FIRE:
                actions.append(('fire', ownId))

            if e.key == pygame.K_RETURN:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_LALT or mods & pygame.KMOD_RALT:
                    toggleFullscreen()

        if e.type == pygame.KEYUP:
            if e.key in KEYS_LEFT:
                actions.append(('stop-left', ownId))
            if e.key in KEYS_RIGHT:
                actions.append(('stop-right', ownId))
            if e.key in KEYS_UP:
                actions.append(('stop-up', ownId))
            if e.key in KEYS_DOWN:
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

    seconds = int(tick / 60)
    minutes = int(seconds / 60)
    matchtime = '%02i:%02i' % (minutes, seconds % 60)

    font.drawText(screen, 'Pts: ' + str(gamestate.points), 31, 2, fgcolor=(255,255,255))
    font.drawText(screen, matchtime, 34, 20, fgcolor=(255,255,255))

    # render level
    for y in range(LEV_H):
        for x in range(LEV_W):
            if gamestate.getLevel()[y][x] == '#':
                screen.blit(tiles['#'], (x * TILE_W, y * TILE_H))
            elif gamestate.getLevel()[y][x] == '.':
                screen.blit(tiles['.'], (x * TILE_W, y * TILE_H))

    # render players
    for obj in gamestate.objects.values():
        obj.draw(screen, tiles)

def update():
    global actions, gamestate, ownPlayer

    if net is None or net.isHost():
        for obj in gamestate.objects.values():
            obj.update(gamestate)

    if net is not None:
        gamestate, actions = net.update(gamestate, actions)
        ownPlayer = gamestate.objects.get(ownId)

    for action, objId in actions:
        if action == 'create-player':
            createPlayer(objId)
            continue

        obj = gamestate.objects.get(objId)

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
        elif action == 'fire':
            obj.interact(gamestate)

    actions = []


def init():
    global gamestate

    worm   = Worm(math.floor(LEV_W/2),math.floor(LEV_H/2))
    ball   = Ball(gamestate)
    bird   = Bird(0,0,'v')

    if net is not None and net.isHost():    # if host doesn't want to be a snake, create a normal player instead
        if not args.nosnake:
            gamestate.objects[-1] = worm
        else:
            createPlayer(-1)

    gamestate.objects[-2] = ball
    gamestate.objects[-3] = bird


init()

tick = 0
running = True

sound.playSound('whistle')

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