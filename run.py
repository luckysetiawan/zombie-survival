import pygame
from pygame.locals import *
from constants import *
from player import Player
from nodes import NodeGroup
from zombies import Zombie
from pauser import Pause

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.pause = Pause(True)

    # create background
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("map.txt")
        # set koordinat titik portal
        self.nodes.setPortalPair((0,17), (27,17))
        self.player = Player(self.nodes.getNodeFromTiles(15, 26))
        self.zombie = Zombie(self.nodes.getNodeFromTiles(12, 14), self.player)

    # dipanggil tiap ganti frame (gameloop)
    def update(self):
        # waktu dalam detik
        dt = self.clock.tick(30) / 1000.0
        
        if not self.pause.paused:
            self.player.update(dt)
            self.zombie.update(dt)
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        # cek event tertentu
        self.checkEvents()
        # draw image ke screen
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause.setPause(playerPaused=True)
                    if not self.pause.paused:
                        self.showEntities()
                    else:
                        self.hideEntities()

    def showEntities(self):
        self.player.visible = True

    def hideEntities(self):
        self.player.visible = False

    def render(self):
        # gambar ulang supaya tidak tumpang tindih
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.player.render(self.screen)
        self.zombie.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
