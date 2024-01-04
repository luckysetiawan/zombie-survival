import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Zombie(Entity):
    def __init__(self, node, player=None, ai_method='heuristic'):
        Entity.__init__(self, node)
        self.name = ZOMBIE
        self.color = GREEN
        self.points = 200
        self.goal = Vector2()
        if ai_method == 'heuristic': 
            self.directionMethod = self.goalHeuristic
        else:
            self.directionMethod = self.goalAstar
        self.ai_method = ai_method
        self.player = player
        self.mode = ModeController(self)

        
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is WANDER:
            self.wander()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def wander(self):
        self.goal = Vector2()
        self.directionMethod = self.randomDirection

    def chase(self):
        self.goal = self.player.position
        if self.ai_method == 'heuristic': 
            self.directionMethod = self.goalHeuristic
        else:
            self.directionMethod = self.goalAstar

    # zombie reset when player dies
    def reset(self):
        Entity.reset(self)
        self.points = 200
        if self.ai_method == 'heuristic': 
            self.directionMethod = self.goalHeuristic
        else:
            self.directionMethod = self.goalAstar