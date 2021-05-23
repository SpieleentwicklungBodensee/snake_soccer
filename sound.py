import pygame

sounds = {}

def loadSound(name, filename):
     sound = pygame.mixer.Sound(filename)
     sounds[name] = sound

def playSound(name):
    sounds[name].play()
