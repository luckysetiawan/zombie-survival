import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        # entity terlihat
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)

    #assign start node
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True


    def setPosition(self):
        self.position = self.node.position.copy()
          
    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    # adjust speed berdasarkan ukuran maze
    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    # render jika entity visible
    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)

    # saat entity sampai di sebuah node, pilih arah secara random (basic)
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    # get list valid direction untuk entity
    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            # arah valid
            if self.validDirection(key):
                # bukan kembali ke arah asal
                if key != self.direction * -1:
                    directions.append(key)
        # kosong = jalan buntu, terpaksa balik
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    # pilih arah secara random
    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]

    # tentukan goal secara heuristic
    def goalHeuristic(self, directions):
        distances = []
        # ambil list arah
        for direction in directions:
            # hitung jarak entity ke goal
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]

    # tentukan goal secara a*
    def goalAstar(self, directions):
        distances = []
        # ambil list arah
        for direction in directions:
            # hitung jarak entity ke goal 
            heuristic = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            # hitung cost entity ke node arah 
            cost = self.directions[direction]*TILEWIDTH
            distances.append(heuristic.magnitudeSquared() + cost.magnitudeSquared())

        index = distances.index(min(distances))
        return directions[index]