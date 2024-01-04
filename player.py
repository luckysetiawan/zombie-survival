import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Player(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PLAYER
        self.directions = {
            UP:Vector2(0, -1), 
            DOWN:Vector2(0, 1), 
            LEFT:Vector2(-1, 0), 
            RIGHT:Vector2(1, 0), 
            STOP:Vector2()
        }
        # initial direction
        self.direction = STOP
        self.speed = 100
        # player size
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()
        # target (player's destination)
        self.target = node
        # player life status
        self.alive = True

    # reset on death
    def reset(self):
        Entity.reset(self)
        self.alive = True

    def die(self):
        self.alive = False
        self.direction = STOP
    
    # copy vector position
    def setPosition(self):
        self.position = self.node.position.copy()

    # input keyboard check
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            # if there are 2 portals then it becomes a 2-way portal
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    # draw player
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    # check if the player overshot the target node
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            # if the player's distance is more than 2 nodes return true
            return node2Self >= node2Target
        return False

    # change direction
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    # check keyboard input in the reverse direction
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False
    
    def collideZombie(self, zombie):
        return self.collideCheck(zombie)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False