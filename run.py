import sys
import pygame
from pygame.locals import *
from constants import *
from player import Player
from nodes import NodeGroup
from zombies import Zombie
from pauser import Pause
from text import TextGroup

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.pause = Pause(True)
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()

    def restartGame(self):
        self.lives = 3
        self.pause.paused = True
        self.startGame(ai_method)
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.showText(READYTXT)

    def resetLevel(self):
        self.pause.paused = True
        self.player.reset()
        self.zombie.reset()
        self.textgroup.showText(READYTXT)

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    # create background
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self, ai_method):
        self.setBackground()
        self.nodes = NodeGroup("map.txt")
        # set portal point coordinates
        self.nodes.setPortalPair((0,17), (27,17))
        self.player = Player(self.nodes.getNodeFromTiles(15, 26))
        self.zombie = Zombie(self.nodes.getNodeFromTiles(12, 14), self.player, ai_method)

    # called every frame change (gameloop)
    def update(self):
        # time in seconds
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        if not self.pause.paused:
            self.updateScore(1)
            self.player.update(dt)
            self.zombie.update(dt)
            self.checkZombieEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        # check for specific events
        self.checkEvents()
        # draw image to the screen
        self.render()

    # update score
    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.player.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities()

    def checkZombieEvents(self):
        if self.player.collideZombie(self.zombie) and self.player.alive:
            self.lives -=  1
            self.player.die()
            if self.lives <= 0:
                self.textgroup.showText(GAMEOVERTXT)
                self.pause.setPause(pauseTime=3, func=self.restartGame)
            else:
                self.pause.setPause(pauseTime=3, func=self.resetLevel)


    def showEntities(self):
        self.player.visible = True

    def hideEntities(self):
        self.player.visible = False

    def render(self):
        # redraw so that there is no overlap
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.player.render(self.screen)
        self.zombie.render(self.screen)
        self.textgroup.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    # default method is heuristic
    ai_method = 'heuristic'
    
    # cli argument to choose ai method
    try:
        ai_method = sys.argv[1]
    except:
        print('No argument entered, zombies will use the default heuristic method to chase you, good luck!')

    if ai_method == 'heuristic' or ai_method == 'astar':
        print('Zombies will use ' + ai_method + ' method to chase you, good luck!')
        game = GameController()
        game.startGame(ai_method)
        while True:
            game.update()
    else:
        print('Invalid Argument, use either \'heuristic\' or \'astar\'')
