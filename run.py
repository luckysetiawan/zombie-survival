import pygame
from pygame.locals import *
from constants import *
from player import Player

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.player = Player()

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.player.update(dt)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render(self.screen)
        pygame.display.update()

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.checkEvents()
        self.render()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
