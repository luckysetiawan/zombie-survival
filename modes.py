from constants import *

class MainMode(object):
    # when the zombie starts to wander
    def __init__(self):
        self.timer = 0
        self.wander()

    # zombie mode switching
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is WANDER:
                self.chase()
            elif self.mode is CHASE:
                self.wander()

    def wander(self):
        self.mode = WANDER
        self.time = 5
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

# controlling zombie mode
class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 

    def update(self, dt):
        self.mainmode.update(dt)
        self.current = self.mainmode.mode